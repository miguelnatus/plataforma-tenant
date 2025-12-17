from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from .views import (
    HomeTenantView,
    NewsletterSubscribeView, NewsletterSubscribeDoneView,
    NewsletterConfirmView, NewsletterUnsubscribeView, PostDetailView,
    CourseListView, CourseDetailView, CourseBuyView,
    StudentLoginView, StudentLogoutView, StudentSignupView, SupporterCreateView,
    SupporterSuccessView, 
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

    # --- ROTAS DE AUTENTICAÇÃO ---
    path("login/", StudentLoginView.as_view(), name="login"),
    path("logout/", StudentLogoutView.as_view(), name="logout"),
    path("signup/", StudentSignupView.as_view(), name="signup"),

    # --- ROTAS DE CURSOS ---
    path("cursos/", CourseListView.as_view(), name="course_list"),
    path("cursos/<int:pk>/<slug:slug>/", CourseDetailView.as_view(), name="course_detail"),
    path("cursos/<int:pk>/comprar/", CourseBuyView.as_view(), name="course_buy"), # Rota lógica de compra

    path("apoiadores/", SupporterCreateView.as_view(), name="supporter_add"),
    path("apoiadores/obrigado/", SupporterSuccessView.as_view(), name="supporter_success"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)