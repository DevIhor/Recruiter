import factory
from apps.accounts.models import Profile, User
from base.models import GenderChoices
from factory import fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    """This is a factory for the User model."""

    class Meta:
        model = User

    email = factory.Faker("free_email")
    password = factory.PostGenerationMethodCall("set_password", "1234567890")
    is_active = True


class ProfileFactory(factory.django.DjangoModelFactory):
    """This is a factory for the Profile model."""

    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone_number = factory.Sequence(lambda n: "+380666666%03d" % n)
    gender = fuzzy.FuzzyChoice(GenderChoices)
