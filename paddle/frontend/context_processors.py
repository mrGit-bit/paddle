# absolute path: /workspaces/paddle/paddle/frontend/context_processors.py
from decouple import config


def app_version(request):
    return {"app_version": config("APP_VERSION", default="")}
