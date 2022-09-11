import factory
from apps.candidates.models import Candidate
from base.models import EnglishLevelChoices, GenderChoices
from factory import fuzzy


class CandidateFactory(factory.django.DjangoModelFactory):
    """Factory for generating random Candidates"""

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    date_of_birth = factory.Faker("date_of_birth")
    gender = fuzzy.FuzzyChoice(GenderChoices)
    phone_number = factory.Sequence(lambda n: "+380666666%03d" % n)
    email = factory.Faker("free_email")
    level_of_english = fuzzy.FuzzyChoice(EnglishLevelChoices)

    class Meta:
        model = Candidate
