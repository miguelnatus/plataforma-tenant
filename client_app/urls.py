from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from .views import HomeTenantView
from django.contrib import admin 
from client_app.admin_site import tenant_admin_site

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("admin/", tenant_admin_site.urls),
    path('', HomeTenantView.as_view(), name='home_tenant'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)