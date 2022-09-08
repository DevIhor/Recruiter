from apps.vacancies.api.v1 import views
from django.urls import path

urlpatterns = [
    path("vacancies/", views.VacancyListViewSet.as_view(), name="vacancies"),
    path("vacancy/<int:pk>/", views.VacancyViewSet.as_view(), name="vacancy"),
    path("currencies/", views.CurrencyListViewSet.as_view(), name="currencies"),
    path("currency/<int:pk>/", views.CurrencyViewSet.as_view(), name="currency"),
]
