import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from corsheaders.defaults import default_headers, default_methods
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROJECT_NAME = os.environ.get("PROJECT_NAME")
SITE_URL = os.environ.get("SITE_URL")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG_MODE") == "YES"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")


# Application definition

INSTALLED_APPS = [
    # Default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Installed apps
    "ckeditor",
    "corsheaders",
    "rest_framework",
    "django_filters",
    "django_rest_passwordreset",
    "drf_yasg",
    "import_export",
    "rest_framework_simplejwt",
    "phonenumber_field",
    "storages",
    "taggit",
    # Custom apps
    "apps.accounts",
    "apps.vacancies",
    "apps.candidates",
    "apps.emails",
    "apps.events",
    "apps.resume",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # new
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # new
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": dj_database_url.config(default=os.environ.get("DATABASE_URL")),
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "1/second",
        "user": "10/second",
    },
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=14),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "AUTH_HEADER_TYPES": ("JWT",),
}

AUTH_USER_MODEL = "accounts.User"

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "media/"

USING_AWS_S3_BUCKET_FOR_STORAGE = os.environ.get("USING_AWS_S3_BUCKET_FOR_STORAGE") == "YES"

# Here, the storage location of the media files is determined.
if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
elif USING_AWS_S3_BUCKET_FOR_STORAGE:
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")

    AWS_S3_FILE_OVERWRITE = False  # so that files with the same name are not overwritten.
    AWS_DEFAULT_ACL = None  # file will be private per Amazon???s default.

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
else:
    # For using media on the server, additional server configuration is required.
    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# List of sites from which you can make requests to this project.
# To enable CORS_ALLOWED_ORIGINS, change CORS_ALLOW_ALL_ORIGINS to False
CORS_ALLOW_ALL_ORIGINS = os.environ.get("CORS_ALLOW_ALL_ORIGINS") == "YES"

if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS").split(",")

# Available HTTP methods and headers that are allowed for the actual request.
CORS_ALLOW_METHODS = list(default_methods) + []
CORS_ALLOW_HEADERS = list(default_headers) + []


TAGGIT_CASE_INSENSITIVE = True

# Email
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "emails")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS") == "YES"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# Celery
CELERY_BROKER_URL = os.environ.get("REDIS_URL")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")
CELERY_TASK_TIME_LIMIT = 5 * 60

# SWAGGER
if DEBUG:
    SWAGGER_SETTINGS = {
        "exclude_namespaces": [],
        "USE_SESSION_AUTH": False,
        "PERSIST_AUTH": True,
        "SECURITY_DEFINITIONS": {
            "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
        },
        "SUPPORTED_SUBMIT_METHODS": ["get", "put", "post", "delete", "patch"],
        "SHOW_REQUEST_HEADERS": True,
    }

REDOC_SETTINGS = {
    "LAZY_RENDERING": False,
}
