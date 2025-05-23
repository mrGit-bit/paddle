# path: paddle/config/settings/dev.py
# settings for production
# optimized for PythonAnywhere deployment

from .base import *
from decouple import config, Csv

# Secret key in production settings
# cSpell: disable-next-line
SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# serve static files from staticfiles directory
# this is where collectstatic copies the static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# serve uploaded media files from media directory
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# change "yourdomain.com" to the actual pythonanywhere or server domain
BASE_API_URL = config("BASE_API_URL", default="https://yourdomain.com/api/")
SITE_URL = config("SITE_URL", default="https://yourdomain.com")

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True