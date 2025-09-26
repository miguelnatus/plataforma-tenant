from django.contrib import admin
from .models import SiteSettings, Post

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
    


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at", "created_at")
    list_filter = ("status", "published_at", "created_at")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}