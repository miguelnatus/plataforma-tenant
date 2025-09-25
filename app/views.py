from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

class HomePublicView(View):
    

    template_name = 'homePublicView.html'

    def get(self, request):
        
        return render(request, self.template_name)
        # return render(request, 'painel.html', context)

# def index(request):
#     return HttpResponse("Hello, world. You're at the public home index.")
    # return render(request, 'templates/homePublicView.html')
    # return HttpResponse("Hello, world. You're at the home index.")
