from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


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
    age : int
        age of the candidate
    updated_at : date
        last time Candidate was updated
    created_at : date
        date of creation of the Candidate

    """

    class GenderChoices(models.TextChoices):
        """This class provides enum for gender types."""
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        OTHER = "O", _("Other")
    
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
        blank=True, 
        null=True
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.OTHER,
    )
    phone_number = PhoneNumberField(
        verbose_name=_("Phone number"),
        blank=True,
        db_index=True,
    )
    email = models.EmailField(
        _("Email address"),
        max_length=100,
        blank=True,
        db_index=True,
    )
    notes = models.TextField(
        _("Additional info"),
        max_length=255,
        blank=True,
        null=True,
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

    @property
    def age(self):
        """Return age of the candidate"""
        from datetime import date

        today = date.today()
        month_day = (self.date_of_birth.month, self.date_of_birth.day)
        return today.year - self.date_of_birth.year - ((today.month, today.day) < month_day)

    @property
    def full_name(self):
        """Return full name of the Candidate."""
        return f"{self.name} {self.surname}"

    def __str__(self):
        """Return full name of the Candidate."""
        return self.full_name

    def __repr__(self):
        """Return Candidate name and its id."""
        return f"{self.__class__.__name__}(id={self.id})"
