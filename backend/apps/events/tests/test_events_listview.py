from apps.accounts.factories import ProfileFactory
from apps.events.factories import EventFactory, EventTypeFactory
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class TestEventsListView(TestCase):
    """This class tests ListCreateEventAPIView."""

    def setUp(self) -> None:
        self.profile = ProfileFactory()
        EventTypeFactory.create_batch(2)
        EventFactory.create_batch(4)
        self.user = self.profile.user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_non_authorized(self):
        """Unauthorized user should not be able to get Events."""
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("events:events-list"))

        self.assertEqual(response.status_code, 401)

    def test_get_authorized(self):
        """Authorized user should be able to get Events."""
        response = self.client.get(reverse("events:events-list"))

        self.assertEqual(response.data.get("count"), 4)
        self.assertEqual(response.status_code, 200)

    def test_create_non_authorized(self):
        """Unauthorized user should not be able to create Events."""
        self.client.force_authenticate(user=None)
        event_data = EventFactory.build()
        response = self.client.post(
            path=reverse("events:events-list"),
            data={
                "title": event_data.title,
                "description": event_data.description,
                "event_type": event_data.event_type.id,
                "start_time": event_data.start_time,
                "end_time": event_data.end_time,
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_create_authorized(self):
        """Authorized user should be able to create Events."""
        event_data = EventFactory.build()
        response = self.client.post(
            path=reverse("events:events-list"),
            data={
                "title": event_data.title,
                "description": event_data.description,
                "event_type": event_data.event_type.id,
                "start_time": event_data.start_time,
                "end_time": event_data.end_time,
                "status": event_data.status,
            },
        )

        self.assertEqual(response.status_code, 201)

    def test_create_authorized_wrong_data(self):
        """Authorized user should not be able to create Events with missing data."""
        event_data = EventFactory.build()
        response = self.client.post(
            path=reverse("events:events-list"),
            data={
                "title": event_data.title,
                "end_time": event_data.end_time,
                "status": event_data.status,
            },
        )

        self.assertEqual(response.status_code, 400)
