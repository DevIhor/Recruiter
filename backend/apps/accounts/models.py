from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


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
