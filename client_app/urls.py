from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from .views import HomeTenantView
from django.contrib import admin 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeTenantView.as_view(), name='home_tenant'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)