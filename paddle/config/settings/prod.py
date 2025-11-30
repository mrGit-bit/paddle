# path: paddle/config/settings/prod.py
# Production settings for Oracle Cloud (Oracle Autonomous DB)

from .base import *
from decouple import config, Csv

#######################################
# DJANGO SECURITY & HOST SETTINGS
#######################################

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="127.0.0.1")
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv(), default="http://127.0.0.1:8000")

#######################################
# ORACLE AUTONOMOUS DATABASE SETTINGS
#######################################

DB_HOST = config("ORACLE_DB_HOST")                         # 'adb...oraclecloud.com' or 'localhost' (tunnel)
DB_PORT = config("ORACLE_DB_PORT", default=1522, cast=int) # 1522 for ADB TCPS
DB_SERVICE = config("ORACLE_DB_SERVICE")                   # e.g. gc5f..._tp.adb.oraclecloud.com
SSL_SERVER_DN = config("ORACLE_SSL_SERVER_DN", default="") # optional pinning for direct mode

def build_walletless_tcps_dsn(host: str, port: int, service: str, ssl_dn: str) -> str:
    """
    Build a wallet-less TCPS DSN for python-oracledb (thin driver).
    - If host is localhost/127.0.0.1 (tunnel), disable DN match (dev convenience).
    - If host is a real ADB host, enable DN match (optionally pin with ssl_server_cert_dn).
    """
    is_tunnel = host in ("localhost", "127.0.0.1")

    if is_tunnel:
        security = "(SECURITY=(ssl_server_dn_match=no))"
    else:
        # Minimal secure default:
        security = "(SECURITY=(ssl_server_dn_match=yes))"
        # Optional strict pinning:
        # if ssl_dn:
        #     security = f'(SECURITY=(ssl_server_dn_match=yes)(ssl_server_cert_dn="{ssl_dn}"))'

    dsn = (
        f"(DESCRIPTION="
        f"(RETRY_COUNT=20)"
        f"(RETRY_DELAY=3)"
        f"(ADDRESS=(PROTOCOL=tcps)(HOST={host})(PORT={port}))"
        f"(CONNECT_DATA=(SERVICE_NAME={service}))"
        f"{security}"
        f")"
    )
    return dsn

DSN = build_walletless_tcps_dsn(DB_HOST, DB_PORT, DB_SERVICE, SSL_SERVER_DN)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": DSN,
        "USER": config("ORACLE_DB_USER"),
        "PASSWORD": config("ORACLE_DB_PASSWORD"),
    }
}

#######################################
# SITE & API BASE URL
#######################################

BASE_API_URL = config("BASE_API_URL", default="http://127.0.0.1:8000/api/")
SITE_URL = config("SITE_URL", default="http://127.0.0.1:8000")

#######################################
# STATIC & MEDIA FILES
#######################################

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Hashed names for rotating static files served with NGINX
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


#######################################
# SECURITY HEADERS
#######################################

# In VM prod with HTTPS → set True in .env
# In Codespaces/HTTP → set False in .env to avoid redirect loops
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=True, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)
