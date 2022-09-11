from apps.accounts.factories import ProfileFactory
from apps.candidates.factories import CandidateFactory
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class TestCandidatesListView(TestCase):
    """This class tests ListCreateCandidateAPIView."""

    def setUp(self) -> None:
        self.profile = ProfileFactory()
        self.user = self.profile.user
        CandidateFactory.create_batch(5)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_non_authorized(self):
        """Unauthorized user should not be able to get Candidates."""
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("candidates:candidates-list"))

        self.assertEqual(response.status_code, 401)

    def test_get_authorized(self):
        """Authorized user should be able to get Candidates."""
        response = self.client.get(reverse("candidates:candidates-list"))

        self.assertEqual(response.data.get("count"), 5)
        self.assertEqual(response.status_code, 200)

    def test_create_non_authorized(self):
        """Unauthorized user should not be able to create Events."""
        self.client.force_authenticate(user=None)
        candidate_data = CandidateFactory.build()
        response = self.client.post(
            path=reverse("candidates:candidates-list"),
            data={
                "name": candidate_data.name,
                "surname": candidate_data.surname,
                "gender": candidate_data.gender,
                "phone_number": str(candidate_data.phone_number),
                "email": candidate_data.email,
                "level_of_english": candidate_data.level_of_english,
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_create_authorized(self):
        """Authorized user should be able to create Events."""
        candidate_data = CandidateFactory.build()
        response = self.client.post(
            path=reverse("candidates:candidates-list"),
            data={
                "name": candidate_data.name,
                "surname": candidate_data.surname,
                "gender": candidate_data.gender,
                "phone_number": str(candidate_data.phone_number),
                "email": candidate_data.email,
                "level_of_english": candidate_data.level_of_english,
            },
        )

        self.assertEqual(response.status_code, 201)

    def test_create_authorized_wrong_data(self):
        """Authorized user should not be able to create Events with missing data."""
        candidate_data = CandidateFactory.build()
        response = self.client.post(
            path=reverse("candidates:candidates-list"),
            data={
                "name": candidate_data.name,
            },
        )

        self.assertEqual(response.status_code, 400)
