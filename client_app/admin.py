from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "primary_color")

    def has_add_permission(self, request):
        # Permite adicionar apenas se não existir registro ainda no schema do tenant atual
        from .models import SiteSettings
        return not SiteSettings.objects.exists()

    def changelist_view(self, request, extra_context=None):
        # Se já existir, redireciona para a tela de edição
        from django.shortcuts import redirect
        from .models import SiteSettings
        obj = SiteSettings.objects.first()
        if obj:
            return redirect(f"./{obj.pk}/change/")
        return super().changelist_view(request, extra_context=extra_context)