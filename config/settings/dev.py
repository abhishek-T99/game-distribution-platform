from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

SECRET_KEY = "dev-secret-key"

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.dev.sqlite3',
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# DRF dev settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ]
}
