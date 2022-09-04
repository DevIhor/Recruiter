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


class EmploymentChoices(models.TextChoices):
    """This class provides enum for employment level."""

    FULL_TIME = "FT", _("Full time")
    PART_TIME = "PT", _("Part time")
    OTHER = "OT", _("Other")


class ExperienceChoice(models.TextChoices):
    """This class provides enum for experience level."""

    WITHOUT = "0M", _("Without experience")
    MONTH_3 = "3M", _("3 months")
    MONTH_6 = "6M", _("6 months")
    MONTH_9 = "9M", _("9 months")
    YEAR_1 = "1Y", _("1 year")
    YEAR_1_5 = "1.5Y", _("1,5 year")
    YEAR_2 = "2Y", _("2 years")
    YEAR_3 = "3Y", _("3 years")
    YEAR_4 = "4Y", _("4 years")
    YEAR_5 = "5Y", _("5 years")


class PriorityChoices(models.IntegerChoices):
    """This class provides priorities for events."""

    UNSPECIFIED = 0, _("Unspecified")
    LOW = 1, _("Low")
    MODERATE = 2, _("Moderate")
    HIGH = 3, _("High")
    CRITICAL = 4, _("Critical")

    __empty__ = _("(Unknown)")


class EventStatusChoices(models.IntegerChoices):
    """This class provides statuses for events."""

    CANCELLED = 0, _("Cancelled")
    ACTIVE = 1, _("Active")
    COMPLETED = 2, _("Completed")

    __empty__ = _("(Unspecified)")

