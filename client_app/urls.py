from django.urls import path 
from .views import HomeTenantView
from django.contrib import admin 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeTenantView.as_view(), name='home_tenant'),
]