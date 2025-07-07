# path: paddle/config/settings/dev.py
# settings for development
# environment values loaded from .env

from .base import *
from decouple import config, Csv

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv()) 
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/' # URL prefix for static files
STATICFILES_DIRS = [BASE_DIR / "frontend/static",] # Static path in development

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Local dev API URL & site URL
BASE_API_URL = config("BASE_API_URL", default="http://127.0.0.1:8000/api/")
SITE_URL = config("SITE_URL", default="http://127.0.0.1:8000/")