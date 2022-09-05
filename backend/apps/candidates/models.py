from datetime import date

from base.models import EnglishLevelChoices, GenderChoices
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Candidate(models.Model):
    """
    This class represents a Candidate model, which can be used to create
    candidates, store their contact information and manage them. All extra
    information is stored in the CV.

    Attributes
    ----------
    name : str
        a firstname of the candidate
    surname : str
        a surname of the candidate
    date_of_birth : date
        a date of birth of the candidate
    gender : str
        a gender of the candidate
    phone_number : str
        a contact number of the candidate
    email : str
        a contact email of the candidate
    level_of_english : str
        a candidate's level of English
    notes : str
        additional info about the candidate
    additional_contacts : str
        additional contact info of the candidate
    age : int
        age of the candidate
    updated_at : date
        last time Candidate was updated
    created_at : date
        date of creation of the Candidate

    """

    class Meta:
        """Standard Meta class for Candidate model."""

        ordering = ("surname", "name")

    name = models.CharField(
        _("Firstname"),
        max_length=50,
        db_index=True,
    )
    surname = models.CharField(
        _("Surname"),
        max_length=50,
        db_index=True,
    )
    date_of_birth = models.DateField(
        _("Birth date"),
        validators=[MaxValueValidator(limit_value=date.today)],
        blank=True,
        null=True,
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.OTHER,
    )
    phone_number = PhoneNumberField(
        verbose_name=_("Phone number"),
        unique=True,
        db_index=True,
    )
    email = models.EmailField(
        _("Email address"),
        max_length=100,
        blank=True,
        db_index=True,
    )
    level_of_english = models.CharField(
        verbose_name=_("Level of English"),
        max_length=2,
        choices=EnglishLevelChoices.choices,
        default=EnglishLevelChoices.UNKNOWN,
    )
    notes = models.TextField(
        _("Additional info"),
        max_length=1200,
        blank=True,
        null=True,
    )
    additional_contacts = models.TextField(
        _("Additional contacts"),
        max_length=400,
        blank=True,
        null=True,
        help_text="Here you can store additional contacts, like Skype.",
    )
    updated_at = models.DateTimeField(
        _("Last update"),
        auto_now=True,
        editable=False,
    )
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        editable=False,
    )
    vacancy = models.ManyToManyField(
        "vacancies.Vacancy",
        related_name="vacanciess",
        verbose_name=_("Vacancies"),
        blank=True,
    )

    @property
    def age(self) -> int:
        """Return age of the candidate"""
        if not self.date_of_birth:
            return 0

        today = date.today()
        month_day = (self.date_of_birth.month, self.date_of_birth.day)
        return today.year - self.date_of_birth.year - ((today.month, today.day) < month_day)

    @property
    def full_name(self) -> str:
        """Return full name of the Candidate."""
        return f"{self.name} {self.surname}"

    @property
    def applications_for_vacancies(self) -> str:
        return "; ".join([f"{i.title}" for i in self.vacancy.all()])

    def __str__(self) -> str:
        """Return full name of the Candidate."""
        return self.full_name

    def __repr__(self) -> str:
        """Return Candidate name and its id."""
        return f"{self.__class__.__name__}(id={self.id})"

