from django.shortcuts import render
from django.views import View
from django.utils.text import slugify
from .models import SiteSettings, Post
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
import secrets
from .forms import NewsletterForm
from .models import NewsletterSubscriber

class HomeTenantView(View):
    template_name = "default/homeView.html"

    def get_template_for_tenant(self, request):
        tname = getattr(request.tenant, "schema_name", "default")
        return f"{tname}/homeView.html"

    def get(self, request):
        settings_obj = SiteSettings.objects.first()
        
        # for settings_obj in SiteSettings.objects.all():
        #     print(settings_obj.favicon)
        post = (
            Post.objects.filter(status=Post.PUBLISHED)
            .order_by("-published_at", "-created_at")
            .only("id", "title", "slug", "summary", "published_at", "created_at")
            .first()
        )
        context = {"settings": settings_obj, "post": post}
        tpl = self.get_template_for_tenant(request)
        
        return render(request, tpl, context)

class NewsletterSubscribeView(FormView):
    form_class = NewsletterForm
    template_name = "newsletter/subscribe.html"
    success_url = reverse_lazy("newsletter_subscribe_done")

    def form_valid(self, form):
        email = form.cleaned_data["email"].lower().strip()
        sub, _ = NewsletterSubscriber.objects.get_or_create(email=email)
        if not sub.confirmed:
            sub.conf_num = secrets.token_urlsafe(12)
            sub.save()
            # TODO: enviar e-mail com link:
            # confirm_url = self.request.build_absolute_uri(
            #   reverse("newsletter_confirm") + f"?email={email}&token={sub.conf_num}"
            # )
            # enviar_email(confirm_url)
        return super().form_valid(form)

class NewsletterSubscribeDoneView(View):
    def get(self, request):
        return render(request, "newsletter/subscribe_done.html")

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

