from apps.resume.api.v1.paginators import CustomCVPagination
from apps.resume.api.v1.serializers import (
    CurriculumVitaeListSerializer,
    CurriculumVitaeRUDSerializer,
)
from apps.resume.models import CurriculumVitae
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


class ListCreateCVAPIView(ListModelMixin, CreateModelMixin, GenericViewSet):
    """
    LIST / CREATE view for the CV model.

    API
    -----------
    get:
    Return a list of Events.

    post:
    Create a new Event instance.

    """

    serializer_class = CurriculumVitaeListSerializer
    pagination_class = CustomCVPagination
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        return CurriculumVitae.objects.all().order_by("-id")

    @swagger_auto_schema(operation_description="Upload file...")
    def create(self, request, *args, **kwargs):
        """POST method for our API."""
        return super().create(request, *args, **kwargs)


class RetrieveUpdateDestroyCVView(
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView
):
    """
    GET / UPDATE / DELETE view for the CV model.

    Methods were redefined in order to use them with swagger.

    API
    -----------
    get <id>:
    Return CV with an id.

    put <id>:
    Update CV with an id.

    patch <id>:
    Partialy CV Event with an id.

    delete <id>:
    Delete CV with an id.

    """

    serializer_class = CurriculumVitaeRUDSerializer
    permission_classes = (IsAuthenticated,)
    queryset = CurriculumVitae.objects.all()
    parser_classes = (MultiPartParser,)

    def get(self, request, *args, **kwargs):
        """GET method of the API."""
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Upload file...")
    def put(self, request, *args, **kwargs):
        """PUT method of the API."""
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Upload file...")
    def patch(self, request, *args, **kwargs):
        """PATCH method of the API."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """DELETE method of the API."""
        return self.destroy(request, *args, **kwargs)
