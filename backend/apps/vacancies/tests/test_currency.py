from apps.vacancies.models import Currency
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

UserModel = get_user_model()


class CurrencyTestCase(TestCase):

    def setUp(self):
        """Starts before each test"""

        Currency.objects.create(
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


    # Testing base access
    def test_currencies_url(self):
        """Test of access to the list of currencies"""

        response = self.client.get(reverse("currencies"))
        self.assertEqual(response.status_code, 200)

    def test_currency_url(self):
        """Test of access to single of currency"""

        response_1 = self.client.get(reverse("currency", args=(1,)))
        response_2 = self.client.get(reverse("currency", args=(2,)))
        response_3 = self.client.get(reverse("currency", args=(0,)))
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(response_3.status_code, 404)


    # Testing authorized user
    def test_authorized_user_create_currency(self):
        """Authorized users can create currency"""

        response = self.client.post(
            reverse("currencies"),
            {
                "currency_title": "new_currency",
                "currency_code": "TTT",
                "pk": 2,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_authorized_user_update_currency(self):
        """Authorized users can update currency"""

        response = self.client.patch(
            reverse("currency", args=(1,)),
            {
                "currency_title": "updated_currency",
                "currency_code": "TTT",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_authorized_user_delete_currency(self):
        """Authorized users can delete currency"""

        response = self.client.delete(reverse("currency", args=(1,)))
        self.assertEqual(response.status_code, 204)

    # Testing non-authorized user
    def test_non_authorized_user_create_currency(self):
        """Unauthorized users cannot create currency"""

        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse("currencies"),
            {
                "currency_title": "new_currency",
                "currency_code": "TTT",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_non_authorized_user_update_currency(self):
        """Unauthorized users cannot update currency"""

        self.client.force_authenticate(user=None)
        response = self.client.patch(
            reverse("currency", args=(1,)),
            {
                "currency_title": "updated_currency",
                "currency_code": "TTT",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_non_authorized_user_delete_currency(self):
        """Unauthorized users cannot delete currency"""

        self.client.force_authenticate(user=None)
        response = self.client.delete(reverse("currency", args=(1,)))
        self.assertEqual(response.status_code, 401)
