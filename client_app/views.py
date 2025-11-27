from django.shortcuts import render, get_object_or_404
from django.views import View
from django.utils.text import slugify
from .models import SiteSettings, Post
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
import secrets
from .forms import NewsletterForm
from .models import NewsletterSubscriber
from django.template.loader import select_template
from django.core.mail import send_mail
from urllib.parse import urlparse, parse_qs

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

        print(destaque)

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

