from random import choice
from string import ascii_letters, digits
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

UserModel = get_user_model()


class UserSignUpTestCase(APITestCase):
    """Class for testing user signup api endpoints."""

    @patch("apps.accounts.tasks.send_verification_email.delay")
    def test_user_signup(self, mock_sent_email):
        """Ensure we can create a new inactive user."""

        url = reverse("signup")
        data = {"email": "testuser@ex.com", "password": "random_string"}

        response = self.client.post(url, data, format="json")

        self.assertTrue(mock_sent_email.called)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(UserModel.objects.get(email="testuser@ex.com").is_active, False)

    @patch("apps.accounts.tasks.send_verification_email.delay")
    def test_user_signup_fail(self, mock_sent_email):
        """Ensure we can't create a new user with the existing email address."""

        url = reverse("signup")
        data = {"email": "testuser@ex.com", "password": "random_string"}

        # Method GET is not allowed
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Create the first user
        self.client.post(url, data, format="json")
        self.assertTrue(mock_sent_email.called)

        # Create the user with the same email address
        response = self.client.post(url, data, format="json")
        self.assertEqual(mock_sent_email.call_count, 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def _generate_activation_url(self, user: UserModel, confirmation_token: str = None) -> str:
        """Generate the account activation link with the provided user_id and confirmation_token."""

        if confirmation_token is None:
            confirmation_token = default_token_generator.make_token(user)
        return reverse("email_confirm", kwargs={"user_id": user.id, "token": confirmation_token})

    def test_user_email_confirm(self):
        """Ensure user can activate the account by clicking the activation link."""

        user = UserModel.objects.create_user(email="testuser@ex.com", password="random_string")
        activation_url = self._generate_activation_url(user)

        self.assertEqual(user.is_active, False)
        self.client.get(activation_url)
        self.assertEqual(UserModel.objects.get(email="testuser@ex.com").is_active, True)

    def test_user_email_confirm_fail(self):
        """Ensure user can't activate the account if token is invalid."""

        user = UserModel.objects.create_user(email="testuser@ex.com", password="random_string")
        invalid_token = "".join(choice(ascii_letters + digits) for _ in range(32))
        activation_url = self._generate_activation_url(user=user, confirmation_token=invalid_token)

        self.assertEqual(user.is_active, False)
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserModel.objects.get(email="testuser@ex.com").is_active, False)
