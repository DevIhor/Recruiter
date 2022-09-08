from locale import currency
from rest_framework.test import APIClient
from apps.vacancies.models import Currency, Vacancy
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse


UserModel = get_user_model()


class VacancyTestCase(TestCase):
    """Class for testing Vacancy CRUD api endpoints."""

    def setUp(self):
        Currency.objects.create(pk=1, currency_title="test_currency", currency_code="TST")

    def test_vacancies_url(self):
        response_1 = self.client.get(reverse('vacancies'))
        self.assertEqual(response_1.status_code, 200)
