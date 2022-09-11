from datetime import datetime, timedelta
from random import randint

import factory
from apps.accounts.models import Profile
from apps.events.models import Event, EventType
from base.models import EventStatusChoices
from factory import fuzzy
from pytz import utc


class EventTypeFactory(factory.django.DjangoModelFactory):
    """Factory for generating random EventType"""

    title = factory.Faker("word")

    class Meta:
        model = EventType


class EventFactory(factory.django.DjangoModelFactory):
    """Factory for generating random Events"""

    title = factory.Faker("catch_phrase")
    description = factory.Faker("text", max_nb_chars=500)
    event_type = factory.Iterator(EventType.objects.all())
    priority = fuzzy.FuzzyChoice(EventStatusChoices)
    owner = factory.Iterator(Profile.objects.all())
    start_time = fuzzy.FuzzyDateTime(
        start_dt=datetime.now(utc),
        end_dt=datetime.now(utc) + timedelta(minutes=60),
        force_second=0,
        force_microsecond=0,
    )
    end_time = fuzzy.FuzzyDateTime(
        start_dt=datetime.now(utc) + timedelta(minutes=60),
        end_dt=datetime.now(utc) + timedelta(minutes=randint(60, 600)),
        force_second=0,
        force_microsecond=0,
    )

    class Meta:
        model = Event
