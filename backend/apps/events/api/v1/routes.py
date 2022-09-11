from apps.events.api.v1.views import ListCreateEventAPIView, RetrieveUpdateDestroyEventView
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", ListCreateEventAPIView, basename="events")

urlpatterns = [
    path("", include(router.urls)),
    path(r"<int:pk>/", RetrieveUpdateDestroyEventView.as_view(), name="event-rud-view"),
]
