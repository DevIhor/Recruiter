from apps.resume.api.v1.views import ListCreateCVAPIView, RetrieveUpdateDestroyCVView
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", ListCreateCVAPIView, basename="resumes")

urlpatterns = [
    path("", include(router.urls)),
    path(r"<int:pk>/", RetrieveUpdateDestroyCVView.as_view(), name="resume-rud-view"),
]
