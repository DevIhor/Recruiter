from datetime import date

from base.models import GenderChoices
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from versatileimagefield.fields import VersatileImageField

from .managers import UserManager


class TelegramUsernameValidator(RegexValidator):
    """
    Validator class for telegram username.
    """

    regex = r"^@\w{5,32}$"
    message = _(
        "Enter a valid username. This value must start with `@` sign "
        "and must contain from 5 to 32 characters."
    )


class User(PermissionsMixin, AbstractBaseUser):
    """
    This class defines a custom User model.

    Attributes
    ----------
    email : str
        an email which is used for login, unique
    is_active : bool
        determines whether user is active
    is_staff : bool
        determines whether user has admin rights
    
    Methods
    ----------
    has_group(name: str)
        returns True if user is in group

    """

    email = models.EmailField(
        _("Email address"),
        unique=True,
        db_index=True,
    )

    is_active = models.BooleanField(
        _("Is active"),
        default=False,
    )

    is_staff = models.BooleanField(
        _("Has admin rights"),
        default=False,
    )

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self) -> str:
        """Return readable representation of the model."""
        return f"User {self.id}: {self.email}"

    @property
    def is_admin(self):
        """Has access to the admin site?"""
        return self.is_staff

    def has_group(self, name: str) -> bool:
        """Return True if user is in group"""
        return self.groups.filter(name__in=name).exists()

    def user_groups(self) -> str:
        """Return list of user groups"""
        return ", ".join([group.name for group in self.groups.all()])


class Profile(models.Model):
    """
    A model to represent the user's profile.

    Attributes
    ----------
    user : User
        an instance of the User model the profile refers to
    first_name :
        a first name of the user
    last_name :
        a last name of the user
    date_of_birth :
        a birth date of the user
    gender :
        a gender of the user
    address :
        an address of the user
    phone_number :
        a phone number of the user
    avatar_image :
        a profile image
    linkedin_url :
        url to user's LinkedIn profile
    telegram_username :
        telegram username of the user
    additional_info :
        an additional information about the user
    created_at :
        a date profile was created
    updated_at :
        a date profile was last updated
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_profile",
        db_index=True,
    )
    first_name = models.CharField(_("First Name"), max_length=127, db_index=True)
    last_name = models.CharField(_("Last Name"), max_length=127, db_index=True)
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
    address = models.CharField(
        _("Address"),
        null=True,
        blank=True,
        max_length=255,
    )
    phone_number = PhoneNumberField(verbose_name=_("Phone number"), unique=True)
    avatar_image = VersatileImageField(
        _("Avatar picture"),
        null=True,
        blank=True,
        upload_to="profile_images/",
    )
    linkedin_url = models.URLField(
        _("LinkedIn profile"),
        null=True,
        blank=True,
        max_length=255,
    )
    telegram_username = models.CharField(
        _("Telegram username"),
        null=True,
        blank=True,
        max_length=32,
        validators=[TelegramUsernameValidator()],
    )
    additional_info = models.TextField(
        _("Additional Info"),
        null=True,
        blank=True,
        max_length=1000,
    )
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("first_name", "last_name")

    @property
    def full_name(self) -> str:
        """Return user's full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        """Return user's age."""
        if not self.date_of_birth:
            return 0

        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )

    @property
    def days_on_site(self) -> int:
        """Return the number of days since the profile was created."""
        delta = now() - self.created_at
        return delta.days

    def __str__(self) -> str:
        return self.full_name
