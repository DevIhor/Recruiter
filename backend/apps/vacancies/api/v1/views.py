from apps.vacancies.api.v1.serializers import CurrencySerializer, VacancySerializer
from apps.vacancies.models import Currency, Vacancy
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer


class VacancyListViewSet(ListCreateAPIView):
    """View for create and list views Vacancy endpoint."""

    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [JSONRenderer]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = (
        "type_of_employment",
        "location",
        "english_level",
        "min_experience",
        "is_active",
        "is_salary_show",
    )

    search_fields = ["=title"]


class VacancyViewSet(RetrieveUpdateDestroyAPIView):
    """View for create, update, delete and view single Vacancy endpoint."""

    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [JSONRenderer]


class CurrencyListViewSet(ListCreateAPIView):
    """View for create and list views Currency endpoint."""

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]


class CurrencyViewSet(RetrieveUpdateDestroyAPIView):
    """View for create, update, delete and view single Currency endpoint."""

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
