from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.text import slugify
from .models import SiteSettings, Post, Course, Enrollment, NewsletterSubscriber, Supporter
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
import secrets
from .forms import NewsletterForm, SupporterForm
from django.template.loader import select_template
from django.core.mail import send_mail
from urllib.parse import urlparse, parse_qs
from django.contrib import messages

class HomeTenantView(View):
    def get_template_for_tenant(self, request):
        tname = getattr(request.tenant, "schema_name", "default")
        template = select_template([
            f"{tname}/homeView.html",
            "default/homeView.html",
        ])
        return template.template.name

    def get(self, request):
        settings_obj = SiteSettings.objects.first()

        destaque = (
            Post.objects.filter(status=Post.PUBLISHED, destaque=True)
            .order_by("-published_at", "-created_at")
            .only("id", "title", "slug", "summary", "published_at", "created_at", "cover_image", "video")
            .first()
        )

        print(settings_obj)

        outros_posts = (
            Post.objects.filter(status=Post.PUBLISHED, destaque=False)
            .order_by("-published_at", "-created_at")
            .only("id", "title", "slug", "summary", "published_at", "created_at", "cover_image", "video")[:6]
        )

        context = {
            "settings": settings_obj,
            "post": destaque,
            "posts": outros_posts,
        }
        tpl = self.get_template_for_tenant(request)
        return render(request, tpl, context)
    
class PostDetailView(View):
    def get(self, request, pk, slug):
        post = get_object_or_404(Post, pk=pk, slug=slug, status=Post.PUBLISHED)
        settings_obj = SiteSettings.objects.first()
        tname = getattr(request.tenant, "schema_name", "default")

        video_embed = None
        if post.video:
            url = str(post.video)
            parsed = urlparse(url)

            if "youtube.com" in parsed.netloc and parsed.path == "/watch":
                qs = parse_qs(parsed.query)
                vid = qs.get("v", [None])[0]
                if vid:
                    video_embed = f"https://www.youtube.com/embed/{vid}"
            elif "youtu.be" in parsed.netloc:
                vid = parsed.path.lstrip("/")
                if vid:
                    video_embed = f"https://www.youtube.com/embed/{vid}"
            else:
                video_embed = url
        
        print(video_embed)

        return render(
            request,
            f"{tname}/post_detail.html",
            {"post": post, "settings": settings_obj, "video_embed": video_embed},
        )

class NewsletterSubscribeView(FormView):
    form_class = NewsletterForm
    template_name = "newsletter/subscribe.html"
    success_url = reverse_lazy("newsletter_subscribe_done")

    def form_valid(self, form):
        email = form.cleaned_data["email"].lower().strip()
        sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
        
        if not sub.confirmed:
            sub.conf_num = secrets.token_urlsafe(12)
            sub.save()
            
            # Envio de e-mail de confirmação
            confirm_url = self.request.build_absolute_uri(
               reverse("newsletter_confirm") + f"?email={email}&token={sub.conf_num}"
            )
            
            # Você deve criar templates de e-mail para subject e message
            send_mail(
                subject="Confirme sua inscrição",
                message=f"Olá! Por favor, confirme sua inscrição clicando no link: {confirm_url}",
                from_email=None,  # Usa DEFAULT_FROM_EMAIL de settings.py
                recipient_list=[email],
                fail_silently=False, # Mude para True em produção se preferir
            )
            
        return super().form_valid(form)

class NewsletterSubscribeDoneView(View):
    def get(self, request):
        # Passa o email para a página de confirmação para exibição
        email = request.GET.get('email', '')
        return render(request, "newsletter/subscribe_done.html", {'email': email})

class NewsletterConfirmView(View):
    def get(self, request):
        email = request.GET.get("email", "").lower().strip()
        token = request.GET.get("token", "")
        try:
            sub = NewsletterSubscriber.objects.get(email=email, conf_num=token)
            sub.confirmed = True
            sub.save()
            return render(request, "newsletter/confirm_ok.html", {"email": email})
        except NewsletterSubscriber.DoesNotExist:
            return render(request, "newsletter/confirm_ok.html", {"email": None})

class NewsletterUnsubscribeView(View):
    def get(self, request):
        email = request.GET.get("email", "").lower().strip()
        token = request.GET.get("token", "")
        try:
            sub = NewsletterSubscriber.objects.get(email=email, conf_num=token)
            sub.confirmed = False
            sub.save()
            return render(request, "newsletter/unsub_ok.html", {"email": email})
        except NewsletterSubscriber.DoesNotExist:
            return render(request, "newsletter/unsub_ok.html", {"email": None})

class CourseListView(ListView):
    model = Course
    template_name = "courses/list.html"  # Você precisará criar este template
    context_object_name = "courses"
    queryset = Course.objects.filter(is_active=True)

class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/detail.html" # Você precisará criar este template
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificar se o usuário já comprou o curso
        if self.request.user.is_authenticated:
            context['is_enrolled'] = Enrollment.objects.filter(
                user=self.request.user, 
                course=self.object, 
                paid=True
            ).exists()
        else:
            context['is_enrolled'] = False
        return context

# View simples de compra (apenas matricula o usuário gratuitamente para teste)
# Para produção, você integraria com Stripe/MercadoPago aqui
class CourseBuyView(LoginRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        Enrollment.objects.get_or_create(user=request.user, course=course, defaults={'paid': True})
        # Redireciona para o detalhe já com acesso liberado ou página de sucesso
        return redirect('course_detail', pk=course.pk, slug=course.slug)

# --- AUTENTICAÇÃO ---

class StudentLoginView(LoginView):
    template_name = "registration/login.html" # Padrão Django ou personalize
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('course_list') # Redireciona para lista de cursos após login

class StudentLogoutView(LogoutView):
    next_page = reverse_lazy('home_tenant')

class StudentSignupView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')


class SupporterSuccessView(TemplateView):
    template_name = "supporters/success.html"

class SupporterCreateView(CreateView):
    model = Supporter
    form_class = SupporterForm
    template_name = "supporters/add.html"
    success_url = reverse_lazy('supporter_success') # <--- MUDANÇA AQUI (era 'supporter_add')

    def form_valid(self, form):
        # Não precisamos mais da mensagem de sucesso na mesma tela, pois vai mudar de página
        # Mas se quiser manter no log, pode deixar.
        return super().form_valid(form)