from config.jwt_tokens import jwt_token_obtain, jwt_token_refresh
from config.swagger import swagger_pattern
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    swagger_pattern,
    jwt_token_obtain,
    jwt_token_refresh,
    path("admin/", admin.site.urls),
    path("api/v1/accounts/", include("apps.accounts.api.v1.routes")),
    path("api/v1/vacancies/", include("apps.vacancies.api.v1.routes_vac")),
    path("api/v1/currencies/", include("apps.vacancies.api.v1.routes_curr")),
    path(
        "api/v1/candidates/",
        include(("apps.candidates.api.v1.routes", "candidates"), namespace="candidates"),
    ),
    path("api/v1/events/", include(("apps.events.api.v1.routes", "events"), namespace="events")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
