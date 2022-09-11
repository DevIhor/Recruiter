from apps.accounts.factories import ProfileFactory
from apps.candidates.factories import CandidateFactory
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class TestRetrieveUpdateDestroyCandidatesView(TestCase):
    """This class tests RetrieveUpdateDestroyCandidateView."""

    def setUp(self) -> None:
        self.profile = ProfileFactory()
        CandidateFactory.create_batch(2)
        self.user = self.profile.user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_non_authorized(self):
        """Unauthorized user should not be able to get Candidate."""
        self.client.force_authenticate(user=None)
        response = self.client.get(
            reverse("candidates:candidate-rud-view", kwargs={"pk": 0}),
        )

        self.assertEqual(response.status_code, 401)

    def test_get_authorized(self):
        """Authorized user should be able to get Candidate."""
        candidate = CandidateFactory()
        response = self.client.get(
            reverse("candidates:candidate-rud-view", kwargs={"pk": candidate.id}),
        )

        self.assertEqual(response.status_code, 200)

    def test_patch_authorized(self):
        """Authorized user should be able to update Candidate."""
        candidate = CandidateFactory()
        event_new_data = CandidateFactory.build()
        change_data_response = self.client.patch(
            reverse("candidates:candidate-rud-view", kwargs={"pk": candidate.id}),
            data={
                "email": event_new_data.email,
            },
        )
        get_data_response = self.client.get(
            reverse("candidates:candidate-rud-view", kwargs={"pk": candidate.id}),
        )

        self.assertEqual(change_data_response.status_code, 200)
        self.assertNotEqual(get_data_response.data.get("email"), candidate.email)
        self.assertEqual(get_data_response.data.get("email"), event_new_data.email)

    def test_delete_authorized(self):
        """Authorized user should be able to delete Candidate."""
        candidate = CandidateFactory()
        delete_data_response = self.client.delete(
            reverse("candidates:candidate-rud-view", kwargs={"pk": candidate.id}),
        )
        get_data_response = self.client.get(
            reverse("candidates:candidate-rud-view", kwargs={"pk": candidate.id}),
        )

        self.assertEqual(delete_data_response.status_code, 204)
        self.assertEqual(get_data_response.status_code, 404)
