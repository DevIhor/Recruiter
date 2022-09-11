from apps.candidates.api.v1.filters import CandidateFilter
from apps.candidates.api.v1.paginators import CustomCandidatePagination
from apps.candidates.api.v1.serializers import CandidateListSerializer, CandidateRUDSerializer
from apps.candidates.models import Candidate
from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


class ListCreateCandidateAPIView(ListModelMixin, CreateModelMixin, GenericViewSet):
    """
    LIST / CREATE view for the Candidate model.

    API
    -----------
    get:
    Return a list of Candidates.

    post:
    Create a new Candidate instance.

    """

    serializer_class = CandidateListSerializer
    pagination_class = CustomCandidatePagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CandidateFilter

    def get_queryset(self):
        return (
            Candidate.objects.all()
            .order_by("-surname", "-name")
            .annotate(
                vacancies_count=Count("vacancy"),
            )
        )


class RetrieveUpdateDestroyCandidateView(
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView
):
    """
    GET / UPDATE / DELETE view for the Candidate model.

    Methods were redefined in order to use them with swagger.

    API
    -----------
    get <id>:
    Return Candidate with an id.

    put <id>:
    Update Candidate with an id.

    patch <id>:
    Partialy Update Candidate with an id.

    delete <id>:
    Delete Candidate with an id.

    """

    serializer_class = CandidateRUDSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Candidate.objects.all()

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
