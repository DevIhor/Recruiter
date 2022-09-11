from apps.candidates.api.v1.views import (
    ListCreateCandidateAPIView,
    RetrieveUpdateDestroyCandidateView,
)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", ListCreateCandidateAPIView, basename="candidates")

urlpatterns = [
    path("", include(router.urls)),
    path(r"<int:pk>/", RetrieveUpdateDestroyCandidateView.as_view(), name="candidate-rud-view"),
]
