from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Recruiter",
        default_version="v1",
        description="Recruiter - is system that is supposed to help Recruiters \
            and Talent Sources to find new candidates. It is Python Bootcamp Project. \
            The project is just a REST API service with basic functionality.",
    ),
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
    public=True,
)

swagger_pattern = path(
    "", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"
)
