from apps.accounts.factories import ProfileFactory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class UserRetrieveUpdateDestroyTestCase(APITestCase):
    """Class for testing user detail api endpoint."""

    def setUp(self) -> None:
        """Called before each single test."""

        self.profile = ProfileFactory()
        self.user = self.profile.user
        self.client.force_authenticate(user=self.user)

    def test_not_authorized_get_userdetail(self):
        """Ensure unauthorized user can't get a user detail info."""

        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("user_detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_get_userdetail(self):
        """Ensure authorized user can get a user detail info."""

        response = self.client.get(reverse("user_detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = ProfileFactory().user
        response = self.client.get(reverse("user_detail", kwargs={"pk": user.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_put_userdetail(self):
        """Ensure authorized user can update its profile data."""

        new_profile = ProfileFactory.build()
        response_update_someones_profile = self.client.put(
            reverse("user_detail", kwargs={"pk": 1}),
            data={
                "email": new_profile.user.email,
                "profile_info": {
                    "first_name": new_profile.first_name,
                    "last_name": new_profile.last_name,
                    "address": new_profile.address,
                },
            },
        )
        self.assertEqual(response_update_someones_profile.status_code, status.HTTP_200_OK)

        response_get_profile = self.client.get(reverse("user_detail", kwargs={"pk": 1}))
        self.assertEqual(
            response_get_profile.data.get("profile_info").get("first_name"), new_profile.first_name
        )

        # forbidden to update someone's profile info
        someones_profile = ProfileFactory()
        response_update_someones_profile = self.client.put(
            reverse("user_detail", kwargs={"pk": someones_profile.user.id}),
            data={
                "email": new_profile.user.email,
                "profile_info": {
                    "first_name": new_profile.first_name,
                    "last_name": new_profile.last_name,
                    "address": new_profile.address,
                },
            },
        )
        self.assertEqual(response_update_someones_profile.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_patch_userdetail(self):
        """Ensure authorized user can partially update its profile data."""

        new_profile = ProfileFactory.build()
        response_partial_update_profile = self.client.patch(
            reverse("user_detail", kwargs={"pk": 1}),
            data={
                "profile_info": {
                    "last_name": new_profile.last_name,
                },
            },
        )
        self.assertEqual(response_partial_update_profile.status_code, status.HTTP_200_OK)

        response_get_profile = self.client.get(reverse("user_detail", kwargs={"pk": 1}))
        self.assertEqual(
            response_get_profile.data.get("profile_info").get("last_name"), new_profile.last_name
        )

        # forbidden to partially update someone's profile info
        someones_profile = ProfileFactory()
        response_partial_update_someones_profile = self.client.patch(
            reverse("user_detail", kwargs={"pk": someones_profile.user.id}),
            data={
                "profile_info": {
                    "last_name": new_profile.last_name,
                },
            },
        )
        self.assertEqual(
            response_partial_update_someones_profile.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_authorized_delete_userdetail(self):
        """Ensure authorized user can delete its account (set inactive)."""

        response_delete_profile = self.client.delete(reverse("user_detail", kwargs={"pk": 1}))
        self.assertEqual(response_delete_profile.status_code, status.HTTP_204_NO_CONTENT)

        response_get_profile_data = self.client.get(reverse("user_detail", kwargs={"pk": 1}))
        self.assertEqual(response_get_profile_data.status_code, status.HTTP_404_NOT_FOUND)
