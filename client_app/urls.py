from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from .views import (
    HomeTenantView,
    NewsletterSubscribeView, NewsletterSubscribeDoneView,
    NewsletterConfirmView, NewsletterUnsubscribeView, PostDetailView 
)
from .admin_site import tenant_admin_site

urlpatterns = [
    # URL do admin aponta para o admin site personalizado do tenant
    path("admin/", tenant_admin_site.urls),
    path("", HomeTenantView.as_view(), name="home_tenant"),
    path("post/<int:pk>/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("newsletter/subscribe/", NewsletterSubscribeView.as_view(), name="newsletter_subscribe"),
    path("newsletter/subscribe/done/", NewsletterSubscribeDoneView.as_view(), name="newsletter_subscribe_done"),
    path("newsletter/confirm/", NewsletterConfirmView.as_view(), name="newsletter_confirm"),
    path("newsletter/unsubscribe/", NewsletterUnsubscribeView.as_view(), name="newsletter_unsubscribe"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)