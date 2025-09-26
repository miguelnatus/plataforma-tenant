from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=120)
    primary_color = models.CharField(max_length=7, default="#0ea5e9")
    logo = models.ImageField(upload_to="branding/", null=True, blank=True)
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)

    def __str__(self):
        return self.site_name