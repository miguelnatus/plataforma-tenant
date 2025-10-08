from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("client_app.urls")),
    path("ckeditor/", include('ckeditor_uploader.urls')),
]