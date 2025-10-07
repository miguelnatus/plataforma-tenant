from django.contrib.admin import AdminSite

class TenantAdminSite(AdminSite):
    site_header = "Solvere ERP"
    site_title = "Solvere ERP"

    def each_context(self, request):
        ctx = super().each_context(request)
        tenant = getattr(request, "tenant", None)
        ctx.update({
            "tenant_name": getattr(tenant, "name", ""),
            "tenant_logo_url": getattr(getattr(tenant, "logo", None), "url", ""),
            "tenant_brand_color": getattr(tenant, "brand_color", "#0D2B4F"),
        })
        return ctx

tenant_admin_site = TenantAdminSite()