from unittest.mock import patch

from apps.accounts.factories import UserFactory
from django.contrib.auth import get_user_model
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

UserModel = get_user_model()


class UserResetPasswordTestCase(APITestCase):
    """Class for testing user password reset endpoints."""

    def setUp(self) -> None:
        """Called before each single test. Create a new user."""

        self.user = UserFactory.create()
        self.request_password_reset_url = reverse("password_reset:reset-password-request")
        self.confirm_password_reset_url = reverse("password_reset:reset-password-confirm")

    @patch("apps.accounts.tasks.send_email_to_user.delay")
    def test_user_request_password_reset(self, mock_sent_email):
        """Ensure user can make a request for the password reset."""

        data = {"email": self.user.email}
        response = self.client.post(self.request_password_reset_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock_sent_email.called)
        self.assertEqual(mock_sent_email.call_count, 1)

    def test_user_request_password_reset_fail(self):
        """
        Ensure user can't make a request for the password reset
        by providing an invalid email address.
        """

        data = {"email": "invalid_email_address@ex.com"}
        response = self.client.post(self.request_password_reset_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_confirm_password_reset(self):
        """Ensure user can set a new password with a valid token."""

        token = ResetPasswordToken.objects.create(user=self.user)
        data = {"token": token.key, "password": "new_password_string"}
        response = self.client.post(self.confirm_password_reset_url, data, format="json")
        self.user = UserModel.objects.get(email=self.user.email)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.check_password("1234567890"), False)

    def test_user_confirm_password_reset_fail(self):
        """Ensure user can't set a new password with an invalid token."""

        data = {"token": "invalid_token_string", "password": "new_random_password"}
        response = self.client.post(self.confirm_password_reset_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.user.check_password("new_random_password"), False)
