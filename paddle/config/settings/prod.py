# path: paddle/config/settings/prod.py
# Production settings for Oracle Cloud (Autonomous DB with private VCN access)
import oracledb
from .base import *
from decouple import config, Csv

# For parsing database URL like Supabase
# import dj_database_url

# --- SECURITY ---
# cSpell: disable-next-line
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="your-vm-ip")
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS", cast=Csv(), default="https://your-vm-ip"
)

# --- DATABASE (Oracle Autonomous DB over private VCN) ---
# Build DSN (Database Service Name, where and how to connect to the database)
dsn = (
    f"(DESCRIPTION="
    f"(ADDRESS=(PROTOCOL=tcps)(HOST={config('ORACLE_DB_HOST')})(PORT={config('ORACLE_DB_PORT')}))"
    f"(CONNECT_DATA=(SERVICE_NAME={config('ORACLE_DB_SERVICE')}))"
    f"(SECURITY=(ssl_server_dn_match=yes)))"
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": dsn,
        "USER": config("ORACLE_DB_USER"),
        "PASSWORD": config("ORACLE_DB_PASSWORD"),
    }
}

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
# import dj_database_url
# DATABASES = {
#     "default": dj_database_url.config(default=config("DATABASE_URL"))
# }

# --- STATIC & MEDIA FILES ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- BASE URL CONFIGURATION ---
BASE_API_URL = config("BASE_API_URL", default="http://your-vm-ip/api/")
SITE_URL = config("SITE_URL", default="http://your-vm-ip")

# --- SECURITY HEADERS ---
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
