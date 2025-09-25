from django.urls import path 
from .views import HomeTenantView 

urlpatterns = [
    path('', HomeTenantView.as_view(), name='home_tenant'),
]