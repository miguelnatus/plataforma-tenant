from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import SiteSettings


class HomeTenantView(View):

    def get(self, request):
        settings_obj = SiteSettings.objects.first()

        for field in SiteSettings._meta.fields:
            print(f"{field.name}: {getattr(settings_obj, field.name)}")

        # print("Site Settings:", settings_obj)

        return render(request, f'{request.tenant}/homeView.html')

# def index(request):
#     return HttpResponse(f"<h1>{request.tenant.schema_name} - {request.tenant.name}</h1>")

