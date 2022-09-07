from unittest.mock import patch

import requests_mock
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

UserModel = get_user_model()


class UserLoginTestCase(APITestCase):
    """Class for testing user login api endpoints."""

    def setUp(self) -> None:
        """
        Called before each single test.
        Create two users: with active account and not activated one.
        """

        users = []
        users_credentials = []
        for i in range(1, 3):
            user_credentials = {"email": f"testuser{i}@ex.com", "password": "random_string"}
            users_credentials.append(user_credentials)
            user = UserModel.objects.create(**user_credentials)
            users.append(user)

        self.user1, self.user2 = users
        self.user1_credentials, self.user2_credentials = users_credentials

        self.user2.is_active = True
        self.user2.save()

        self.login_url = reverse("login")

    @requests_mock.Mocker()
    def test_user_login(self, mock):
        """Ensure user can obtain JWT token by providing existing credentials."""

        url = reverse("token_obtain_pair")
        data = {"access": "random_access_token", "refresh": "random_refresh_token"}
        mock.post(url, json=data, status_code=200)

        response = self.client.post(self.login_url, self.user2_credentials, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {"access": "random_access_token", "refresh": "random_refresh_token"}
        )

    @patch("apps.accounts.tasks.send_verification_email.delay")
    def test_user_login_fail(self, mock_sent_email):
        """
        Ensure user cannot obtain JWT token by providing invalid credentials or
        user's account is inactive.
        """

        invalid_credentials = {"email": "invalid_email@ex.com", "password": "invalid_password"}

        response = self.client.post(self.login_url, invalid_credentials, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Account is not activated
        response = self.client.post(self.login_url, self.user1_credentials, format="json")
        self.assertTrue(mock_sent_email.called)
        self.assertEqual(mock_sent_email.call_count, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
