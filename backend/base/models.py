from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderChoices(models.TextChoices):
    """This class provides enum for gender types."""

    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
    OTHER = "O", _("Other")


class EnglishLevelChoices(models.TextChoices):
    """This class provides enum for levels of English."""

    UNKNOWN = "A0", _("Unknown")
    BEGINNER = "A1", _("Beginner")
    ELEMENTARY = "A2", _("Elementary")
    INTERMEDIATE = "B1", _("Intermediate")
    UPPER_INTERMEDIATE = "B2", _("Upper-intermediate")
    ADVANCED = "C1", _("Advanced")
    PROFICIENCY = "C2", _("Proficiency")
