from apps.vacancies.api.v1 import views
from django.urls import path

urlpatterns = [
    path("", views.CurrencyListViewSet.as_view(), name="currencies"),
    path("<int:pk>", views.CurrencyViewSet.as_view(), name="currency"),
]
