import os
from datetime import timedelta

from django.conf import settings

settings.configure(ROOT_URLCONF=__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get Django environment set by docker (i.e either development or production), or else set it to local

DJANGO_ENV = os.environ.get("DJANGO_ENV", "local")

# If Django environement has been set by docker it would be
# either development or production otherwise it would be undefined or local

SECRET_KEY = os.environ.get("SECRET_KEY", "localsecret")
DEBUG = bool(int(os.environ.get("DEBUG", default=0)))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1 0.0.0.0 localhost").split(" ")

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DB_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("DB_USER", "user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "password"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# (CORS) Cross-Origin Resource Sharing Settings
CORS_ORIGIN_ALLOW_ALL = True

# STATIC FILES ROOT AND URL

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "static/"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_LIFETIME", 10))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.environ.get("REFRESH_TOKEN_LIFETIME", 1))),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}
