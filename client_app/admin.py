from .admin_site import tenant_admin_site
from .models import SiteSettings, Post
from django.contrib import admin

@admin.register(SiteSettings, site=tenant_admin_site)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "primary_color")
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        obj = SiteSettings.objects.first()
        if obj:
            return redirect(f"./{obj.pk}/change/")
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Post, site=tenant_admin_site)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at", "created_at")
    list_filter = ("status", "published_at", "created_at")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}