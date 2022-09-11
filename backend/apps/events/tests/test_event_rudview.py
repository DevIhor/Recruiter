from apps.accounts.factories import ProfileFactory
from apps.events.factories import EventFactory, EventTypeFactory
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class TestRetrieveUpdateDestroyEventView(TestCase):
    """This class tests RetrieveUpdateDestroyEventView."""

    def setUp(self) -> None:
        self.profile = ProfileFactory()
        EventTypeFactory.create_batch(2)
        self.user = self.profile.user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_non_authorized(self):
        """Unauthorized user should not be able to get Event."""
        self.client.force_authenticate(user=None)
        response = self.client.get(
            reverse("events:event-rud-view", kwargs={"pk": 0}),
        )

        self.assertEqual(response.status_code, 401)

    def test_get_authorized(self):
        """Authorized user should be able to get Event."""
        event = EventFactory()
        response = self.client.get(
            reverse("events:event-rud-view", kwargs={"pk": event.id}),
        )

        self.assertEqual(response.status_code, 200)

    def test_patch_authorized(self):
        """Authorized user should be able to update Event."""
        event = EventFactory()
        event_new_data = EventFactory.build()
        change_data_response = self.client.patch(
            reverse("events:event-rud-view", kwargs={"pk": event.id}),
            data={
                "description": event_new_data.description,
            },
        )
        get_data_response = self.client.get(
            reverse("events:event-rud-view", kwargs={"pk": event.id}),
        )

        self.assertEqual(change_data_response.status_code, 200)
        self.assertNotEqual(get_data_response.data.get("description"), event.description)
        self.assertEqual(get_data_response.data.get("description"), event_new_data.description)

    def test_delete_authorized(self):
        """Authorized user should be able to delete Event."""
        event = EventFactory()
        delete_data_response = self.client.delete(
            reverse("events:event-rud-view", kwargs={"pk": event.id}),
        )
        get_data_response = self.client.get(
            reverse("events:event-rud-view", kwargs={"pk": event.id}),
        )

        self.assertEqual(delete_data_response.status_code, 204)
        self.assertEqual(get_data_response.status_code, 404)
