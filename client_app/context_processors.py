def tenant_branding(request):
    tenant = getattr(request, "tenant", None)
    return {
        "tenant_name": getattr(tenant, "name", ""),
        "tenant_logo_url": getattr(getattr(tenant, "logo", None), "url", ""),
        "tenant_brand_color": getattr(tenant, "brand_color", "#0D2B4F"),
    }