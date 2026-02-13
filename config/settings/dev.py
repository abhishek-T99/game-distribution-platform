import os

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

SECRET_KEY = "dev-secret-key"

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DEV_DB"],
        "USER": os.environ["POSTGRES_DEV_USER"],
        "PASSWORD": os.environ["POSTGRES_DEV_PASSWORD"],
        "HOST": os.environ.get("POSTGRES_DEV_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_DEV_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# DRF dev settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ]
}
