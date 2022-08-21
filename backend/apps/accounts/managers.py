from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    This class represents a custom User manager.

    Methods
    -------
    create_user(self, email, password, **kwargs):
        creates a new user
    create_superuser(self, email, password, **kwargs):
        creates a new superuser

    """

    def create_user(self, email, password, **kwargs):
        """Creates a new user.

        Attributes
        ----------
        email : str
            email address of the user
        password: str
            password of the user
        kwargs: dict
            additional fields of the user model

        """
        if not email:
            raise ValueError(
                _("Email address is required.")
            )

        user = self.model(
            email=self.normalize_email(email),
            **kwargs,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        """Creates a new superuser.

        Attributes
        ----------
        email : str
            email address of the user
        password: str
            password of the user
        kwargs: dict
            additional fields of the user model

        """
        user = self.create_user(
            email, password, **kwargs
        )
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
