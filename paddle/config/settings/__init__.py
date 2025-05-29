# path: paddle/config/settings/__init__.py
from decouple import config

# Default to 'dev' if DJANGO_ENVIRONMENT is not explicitly set
env = config("DJANGO_ENVIRONMENT", default="dev").lower()
print(f"DJANGO_ENVIRONMENT set to: {env}")
print(f"DEBUG set to: {config('DEBUG', default=True, cast=bool)}")

if env == "prod":
    from .prod import *
elif env == "dev":
    from .dev import *
else:
    raise ValueError(f"Unknown DJANGO_ENVIRONMENT value: '{env}'. Expected 'dev' or 'prod'.")
