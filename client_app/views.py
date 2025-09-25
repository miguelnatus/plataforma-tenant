from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


class HomeTenantView(View):

    def get(self, request):
        return render(request, f'{request.tenant}/homeView.html')

# def index(request):
#     return HttpResponse(f"<h1>{request.tenant.schema_name} - {request.tenant.name}</h1>")

