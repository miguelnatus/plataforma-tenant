from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from embed_video.fields import EmbedVideoField

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=120)
    primary_color = models.CharField(max_length=7, default="#0ea5e9")
    favicon = models.ImageField(upload_to="branding/", null=True, blank=True)
    logo = models.ImageField(upload_to="branding/", null=True, blank=True)
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    profile = models.ImageField(upload_to="branding/", null=True, blank=True)

    def __str__(self):
        return self.site_name
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=32, blank=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Opcional: se quiser isolar por tenant (um e-mail pode se inscrever em múltiplos tenants)
    # tenant = models.ForeignKey("app.Client", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        status = "ok" if self.confirmed else "pendente"
        return f"{self.email} ({status})"
    
class Post(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = [(DRAFT, "Rascunho"), (PUBLISHED, "Publicado")]
    destaque = models.BooleanField(default=False)

    title = models.CharField(max_length=360)
    slug = models.SlugField(max_length=180, unique=True, db_index=True)
    summary = models.CharField(max_length=540, blank=True)
    content = RichTextUploadingField()
    cover_image = models.ImageField(upload_to="posts/", null=True, blank=True)
    video = EmbedVideoField(blank=True, help_text="URL do vídeo (YouTube/Vimeo)")
    # aqui muda:
    # video = models.TextField(
    #     blank=True,
    #     help_text="Cole aqui o código completo do iframe do vídeo (YouTube/Vimeo)",
    # )

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            i = 2
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)