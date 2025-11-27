from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.contrib.admin.widgets import AdminFileWidget
from .models import SiteSettings, NewsletterSubscriber, Post
from .admin_site import tenant_admin_site # Importa o admin site personalizado

class ImagePreviewWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        out = []
        try:
            if hasattr(value, "url") and value:
                out.append(f'<a href="{value.url}" target="_blank">'
                           f'<img src="{value.url}" style="height:40px;object-fit:contain;border:1px solid #ddd;padding:2px;border-radius:4px"/></a>')
        except Exception:
            pass
        out.append(super().render(name, value, attrs, renderer))
        return format_html("".join(out))

class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name" ,"primary_color", "favicon_preview", "logo_preview")
    formfield_overrides = {
        models.ImageField: {"widget": ImagePreviewWidget}
    }

    def favicon_preview(self, obj):
        return format_html(f'<img src="{obj.favicon.url}" style="height:24px;object-fit:contain"/>') if obj.favicon else "-"
    favicon_preview.short_description = "favicon"

    def logo_preview(self, obj):
        return format_html(f'<img src="{obj.logo.url}" style="height:24px;object-fit:contain"/>') if obj.logo else "-"
    logo_preview.short_description = "logo"

class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "confirmed", "created_at")
    list_filter = ("confirmed", "created_at")
    search_fields = ("email",)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'destaque', 'published_at', 'created_at')
    list_filter = ('status', 'destaque', 'published_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

# Registra os models no admin site do tenant
tenant_admin_site.register(SiteSettings, SiteSettingsAdmin)
tenant_admin_site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
tenant_admin_site.register(Post, PostAdmin)