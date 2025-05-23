# path: paddle/config/settings/__init__.py
import os

# Default to 'dev' if DJANGO_ENVIRONMENT is not explicitly set
env = os.environ.get("DJANGO_ENVIRONMENT", "dev").lower()

if env == "prod":
    from .prod import *
elif env == "dev":
    from .dev import *
else:
    raise ValueError(f"Unknown DJANGO_ENVIRONMENT value: '{env}'. Expected 'dev' or 'prod'.")
