import os  # noqa

from .base import *  # noqa

# List of sites from which you can make requests to this project.
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
]

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
