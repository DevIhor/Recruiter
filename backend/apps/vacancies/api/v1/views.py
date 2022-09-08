from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from apps.vacancies.api.v1.serializers import VacancySerializer, CurrencySerializer
from apps.vacancies.models import Vacancy, Currency


class VacancyListViewSet(ListCreateAPIView):
    """View for create and list views Vacancy endpoint."""

    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [
        DjangoFilterBackend, 
        SearchFilter, 
        OrderingFilter
        ]
    filterset_fields = (
        "type_of_employment", 
        "location", 
        "english_level", 
        "min_experience", 
        "is_active", 
        "is_salary_show", 
        )
    
    search_fields = ['=title']



class VacancyViewSet(RetrieveUpdateDestroyAPIView):
    """View for create, update, delete and view single Vacancy endpoint."""

    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CurrencyListViewSet(ListCreateAPIView):
    """View for create and list views Currency endpoint."""

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CurrencyViewSet(RetrieveUpdateDestroyAPIView):
    """View for create, update, delete and view single Currency endpoint."""

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

