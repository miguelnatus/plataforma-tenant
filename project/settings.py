import os
from pathlib import Path
import environ

# Base
BASE_DIR = Path(__file__).resolve().parent.parent

# .env
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Segurança e debug
SECRET_KEY = env("SECRET_KEY")  # defina no .env
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["annasebba.com.br", "www.annasebba.com.br", "127.0.0.1", "localhost"],
)
# Proteções de CSRF (exigem esquema)
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["https://annasebba.com.br", "https://www.annasebba.com.br"],
)

# Apps (multi-tenant + admin com Jazzmin)
SHARED_APPS = [
    "jazzmin",                      # Jazzmin antes do admin
    "django_tenants",               # Multi-tenant (schemas)
    "app",                          # App público/compartilhado (TENANT_MODEL/TENANT_DOMAIN_MODEL)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",# WhiteNoise desabilita static do runserver
    "django.contrib.staticfiles",
]

TENANT_APPS = [
    "client_app",                   # App específico dos tenants
    "ckeditor",
    "ckeditor_uploader",
    "embed_video",
]

INSTALLED_APPS = SHARED_APPS + [a for a in TENANT_APPS if a not in SHARED_APPS]

# Middleware
MIDDLEWARE = [
    # Recomendado pelo projeto: main.TenantMainMiddleware no topo
    "django_tenants.middleware.main.TenantMainMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # servir estáticos em prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"
PUBLIC_SCHEMA_URLCONF = "app.urls"  # URLs do schema público

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # ex.: [BASE_DIR / "templates"]
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",   # necessário p/ tenants
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "client_app.context_processors.tenant_branding",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"
SILENCED_SYSTEM_CHECKS = ['ckeditor.W001']
# Banco (PostgreSQL + django-tenants)
DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE", default="django_tenants.postgresql_backend"),
        "NAME": env("DATABASE_DB", default="plataforma_user"),
        "USER": env("DATABASE_USER", default="postgres"),
        "PASSWORD": env("DATABASE_PASSWORD", default=""),
        "HOST": env("DATABASE_HOST", default="127.0.0.1"),
        "PORT": env("DATABASE_PORT", default="5432"),
        "CONN_MAX_AGE": env.int("CONN_MAX_AGE", default=300),
        "OPTIONS": {"sslmode": env("DB_SSLMODE", default="disable")},
    }
}
DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)

# Modelos de tenant (ajuste para o caminho real dos seus models)
TENANT_MODEL = "app.Client"
TENANT_DOMAIN_MODEL = "app.Domain"

# Internacionalização
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Arquivos estáticos e mídia
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = []  # ex.: [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Senhas
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "Anna Sebba",
    "site_header": "Anna Sebba",
    "site_brand": "Anna Sebba",
    "site_logo": None,  # logo por tenant via template/context
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "products.Brand": "fas fa-copyright",
        "products.Category": "fas fa-object-group",
        "products.Product": "fas fa-box",
    },
    "welcome_sign": "Bem-vindo(a) ao Solvere ERP",
    "show_ui_builder": True,
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "minty",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

# CKEditor
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": "100%",
    },
}
CKEDITOR_CONFIGS['default']['extraAllowedContent'] = 'iframe[*]' 