from datetime import date, timedelta

from apps.vacancies.models import Currency, Vacancy
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


UserModel = get_user_model()


class VacancyTestCase(TestCase):
    """Class for testing Vacancy CRUD api endpoints."""

    def setUp(self):
        """Starts before each test"""

        self.curr = Currency.objects.create(
            pk=1, 
            currency_title="test_currency", 
            currency_code="TST"
        )

        self.user = UserModel.objects.create(
            email="test@test.com", 
            is_active=True, 
            is_staff=True, 
            password="secret_password"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        Vacancy.objects.create(
            title="Test developer",
            keywords="keyword1, keyword2",
            type_of_employment="FT",
            location="remote",
            english_level="B1",
            min_experience="2Y",
            end_date=date.today() + timedelta(days=14),
            start_date=date.today(),
            description="Some large text",
            priority="Also some large text",
            salary_max=2000,
            salary_min=1500,
            salary_currency=self.curr,
            author=self.user,
            contact_person=self.user,
            is_active=True,
            is_salary_show=True,
        )

        self.vacancy_data = {
            "title": "Test developer 2",
            "keywords": ["keyword1", "keyword2", "keyword3"],
            "type_of_employment": "PT",
            "location": "City, remote",
            "english_level": "A1",
            "min_experience": "3M",
            "end_date": "2022-09-30",
            "start_date": "2022-09-15",
            "description": "Some large text",
            "priority": "Also some large text",
            "salary_max": 1000,
            "salary_min": 800,
            "salary_currency": 1,
            "author": 1,
            "contact_person": 1,
            "is_active": True,
            "is_salary_show": False,
        }


    # Testing base access
    def test_vacancies_url(self):
        """Test of access to the list of vacancies"""

        response_1 = self.client.get(reverse("vacancies"))
        self.assertEqual(response_1.status_code, 200)


    def test_vacancy_url(self):
        """Test of access to single of vacancy"""

        response_1 = self.client.get(reverse("vacancy", args=(1,)))
        response_2 = self.client.get(reverse("vacancy", args=(2,)))
        response_3 = self.client.get(reverse("vacancy", args=(0,)))
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(response_3.status_code, 404)


    # Testing authorized user
    def test_authorized_user_create_vacancy(self):
        """Authorized users can create vacancy"""

        response = self.client.post(
            reverse("vacancies"), 
            self.vacancy_data, 
            format="json"
        )
        self.assertEqual(response.status_code, 201)


    def test_authorized_user_create_vacancy_wrong_salary(self):
        """Authorized users cannot create wrong vacancy (wrong salary)"""


        self.vacancy_data["salary_min"] = 1500
        response = self.client.post(
            reverse("vacancies"), 
            self.vacancy_data, 
            format="json"
        )
        self.assertEqual(response.status_code, 400)


    def test_authorized_user_create_vacancy_wrong_date(self):
        """Authorized users cannot create wrong vacancy (wrong date)"""

        self.vacancy_data["start_date"] = "2022-10-15"
        response = self.client.post(
            reverse("vacancies"), 
            self.vacancy_data, 
            format="json"
        )
        self.assertEqual(response.status_code, 400)


    def test_authorized_user_update_vacancy(self):
        """Authorized users can update vacancy"""

        self.vacancy_data["title"] = "Updated Test developer"
        response = self.client.patch(
            reverse("vacancy", args=(1,)), 
            self.vacancy_data, 
            format="json"
        )
        self.assertEqual(response.status_code, 200)


    def test_authorized_user_update_vacancy_wrong_salary(self):
        """Authorized users cannot update vacancy by wrong salary"""

        self.vacancy_data["salary_min"] = 20000
        response = self.client.patch(
            reverse("vacancy", args=(1,)), 
            self.vacancy_data, 
            format="json"
        )
        self.assertEqual(response.status_code, 400)


    def test_authorized_user_update_vacancy_wrong_date(self):
        """Authorized users cannot update vacancy by wrong date"""

        self.vacancy_data["end_date"] = "1900-10-15"
        response = self.client.patch(
            reverse("vacancy", args=(1,)), 
            self.vacancy_data, 
            format="json"
        )
        self.assertEqual(response.status_code, 400)


    def test_authorized_user_delete_vacancy(self):
        """Authorized users can delete vacancy"""

        response = self.client.delete(reverse("vacancy", args=(1,)))
        self.assertEqual(response.status_code, 204)


    # Testing non-authorized user
    def test_non_authorized_user_create_vacancy(self):
        """Unauthorized users cannot create vacancy"""

        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse("vacancies"), 
            self.vacancy_data, 
            format="json"
        )
        self.assertEqual(response.status_code, 401)


    def test_non_authorized_user_update_vacancy(self):
        """Unauthorized users cannot update vacancy"""

        self.vacancy_data["title"] = "Updated Test developer"
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            reverse("vacancy", args=(1,)), 
            self.vacancy_data, 
            format="json"
        )
        self.assertEqual(response.status_code, 401)


    def test_non_authorized_user_delete_vacancy(self):
        """Unauthorized users cannot update vacancy"""

        self.client.force_authenticate(user=None)
        response = self.client.delete(reverse("vacancy", args=(1,)))
        self.assertEqual(response.status_code, 401)
