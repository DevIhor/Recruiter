from apps.events.api.v1.filters import EventFilter
from apps.events.api.v1.paginators import CustomEventPagination
from apps.events.api.v1.serializers import EventListSerializer, EventRUDSerializer
from apps.events.models import Event
from django.db.models import Case, Count, When
from django.db.utils import IntegrityError
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ListCreateEventAPIView(ListModelMixin, CreateModelMixin, GenericViewSet):
    """
    LIST / CREATE view for the Event model.

    API
    -----------
    get:
    Return a list of Events.

    post:
    Create a new Event instance.

    """

    serializer_class = EventListSerializer
    pagination_class = CustomEventPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter

    def get_queryset(self):
        current_time = timezone.now()
        return (
            Event.objects.all()
            .order_by("start_time")
            .annotate(
                visitors=Count("staff_participants") + Count("candidate_participants"),
                is_future=Case(When(start_time__gt=current_time, then=True), default=False),
            )
        )

    def create(self, request, *args, **kwargs):
        """Check that none of the db constraints was violated."""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError:
            return Response(
                data={
                    "message": "Can't create event if it's end time is greater than "
                    "it's start time."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_create(self, serializer):
        """Create an Event and assign the Profile of the User as an owner of the Event."""
        serializer.save(owner=self.request.user.user_profile)


class RetrieveUpdateDestroyEventView(
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView
):
    """
    GET / UPDATE / DELETE view for the Event model.

    Methods were redefined in order to use them with swagger.

    API
    -----------
    get <id>:
    Return Event with an id.

    put <id>:
    Update Event with an id.

    patch <id>:
    Partialy Update Event with an id.

    delete <id>:
    Delete Event with an id.

    """

    serializer_class = EventRUDSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()

    def get(self, request, *args, **kwargs):
        """GET method of the API."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """PUT method of the API."""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """PATCH method of the API."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """DELETE method of the API."""
        return self.destroy(request, *args, **kwargs)
