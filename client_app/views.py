from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import SiteSettings, Post

class HomeTenantView(View):
    def get(self, request):
        # Idealmente, configurações por tenant (ex.: OneToOne com Tenant)
        # settings_obj = SiteSettings.objects.filter(tenant=request.tenant).first()
        # for field in SiteSettings._meta.fields:
        post = Post.objects.filter(status=Post.PUBLISHED).first()
        print(post)
        for post in Post.objects.filter(status=Post.PUBLISHED):
            print(f"{post.title}: {post.slug} - {post.content} - {post.created_at}  ")
            
        settings_obj = SiteSettings.objects.first()

        context = {
            "settings": settings_obj,  # acessa no template como settings.logo, settings.primary_color etc.
            "post": post,
        }
        return render(request, f'{request.tenant}/homeView.html', context)
# class HomeTenantView(View):

#     def get(self, request):
#         settings_obj = SiteSettings.objects.first()

#         for field in SiteSettings._meta.fields:
#             # print(f"{field.name}: {getattr(settings_obj, field.name)}")
#             print(settings_obj.logo)
#         # print("Site Settings:", settings_obj)

#         return render(request, f'{request.tenant}/homeView.html')
    
   

# def index(request):
#     return HttpResponse(f"<h1>{request.tenant.schema_name} - {request.tenant.name}</h1>")

