from .views import HomePublicView   
from django.urls import path 
from django.contrib import admin 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePublicView.as_view(), name='home_public'),
]