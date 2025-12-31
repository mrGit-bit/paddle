# path: paddle/config/settings/base.py
# common settings for development and production
# specific settings are in dev.py and prod.py
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",    
    "users",
    "games",
    "frontend",
    "americano",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",    
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware", # Ensure locale is set
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "frontend/templates"], # Ensure templates are found
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "americano.context_processors.americano_nav",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth", 
                "django.template.context_processors.csrf", # Ensure CSRF token is available
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"




# Password validation
# Shared security policy (not environment-specific)
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
# Spanish-only for visible texts
LANGUAGE_CODE = "es"  # Language code for visible texts
TIME_ZONE = "Europe/Madrid"  # Time zone for date and time calculations
USE_I18N = True  # Enable internationalization
USE_TZ = True  # Enable time zone usage
USE_THOUSAND_SEPARATOR = True  # Enable thousands separator
THOUSAND_SEPARATOR = "."  # Thousands separator
DECIMAL_SEPARATOR = ","  # Decimal separator
LANGUAGES = [("es", "Español")]  # Available languages
LOCALE_PATHS = [BASE_DIR / "locale"]  # Path to translation files

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Rest Framework Settings
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 12,  # Display 12 items per page (multiple of 3 for Bootstrap grid)
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# URL to be redirected after login with api-auth/
LOGIN_REDIRECT_URL = '/api/games/players/'

# Override the Django´s default login page (/account/login/)
LOGIN_URL = '/login/'

# DRF recognizes the actual domain that was forwarded by the proxy 
# (the GitHub Codespace URL) instead of assuming 127.0.0.1.
USE_X_FORWARDED_HOST = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# --- Email (Brevo SMTP via env) ---
PASSWORD_RESET_TIMEOUT = 60 * 60 * 24  # Password reset token lifetime: 1 day in seconds
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp-relay.brevo.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = f"{config('FROM_NAME', default='Ranking de Pádel')} <{config('DEFAULT_FROM_EMAIL', default='no-reply@rankingdepadel.club')}>"
SERVER_EMAIL = DEFAULT_FROM_EMAIL

