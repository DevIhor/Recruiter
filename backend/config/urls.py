from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .jwt_tokens import jwt_token_obtain, jwt_token_refresh
from .swagger import swagger_pattern

urlpatterns = [
    swagger_pattern,
    jwt_token_obtain,
    jwt_token_refresh,
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
