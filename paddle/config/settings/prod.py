# path: paddle/config/settings/prod.py
# Production settings for Railway and Supabase PostgreSQL

from .base import *
from decouple import config, Csv
import dj_database_url

# Secret key in production settings
# cSpell: disable-next-line
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="glistening-solace.up.railway.app")
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv(), default="https://glistening-solace.up.railway.app")

# # Mysql database and credentials
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": config("MYSQL_DB_NAME"),
#         "USER": config("MYSQL_DB_USER"),
#         "PASSWORD": config("MYSQL_DB_PASSWORD"),
#         "HOST": config("MYSQL_DB_HOST", default="127.0.0.1"),
#         "PORT": config("MYSQL_DB_PORT", default="3306"),
#         "OPTIONS": {
#             "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

# PostgreSQL database and credentials
DATABASES = {
    "default": dj_database_url.config(default=config("DATABASE_URL"))
}

# serve static files from staticfiles directory
# this is where collectstatic copies the static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# serve uploaded media files from media directory
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# change "yourdomain.com" to the actual pythonanywhere or railway domain
BASE_API_URL = config("BASE_API_URL", default="https://your-railway-app.up.railway.app/api/")
SITE_URL = config("SITE_URL", default="https://your-railway-app.up.railway.app")

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

