from apps.accounts.factories import UserFactory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class UserListTestCase(APITestCase):
    """Class for testing user list api endpoint."""

    def setUp(self) -> None:
        """Called before each single test. Create 5 users."""

        self.user = UserFactory.create_batch(5)[0]
        self.user_list_url = reverse("user_list")

    def test_not_authorized_user_get_userlist(self):
        """Ensure unauthorized user can't get a user list."""

        self.client.force_authenticate(user=None)
        response = self.client.get(self.user_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_user_get_userlist(self):
        """Ensure authorized user can get a user list."""

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("count"), 5)
