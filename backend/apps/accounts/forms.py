from django import forms
from .models import User
from django.contrib.auth.forms import (UserCreationForm,
                                       ReadOnlyPasswordHashField,
                                       UserChangeForm as ChangeForm)


class UserCreateForm(UserCreationForm):
    """This class defines form for creating new users."""
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        """Save the provided password in hashed format."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(ChangeForm):
    """A form for updating users."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        """Meta class for specifing CustomUser model and its fields."""

        model = User
        fields = ("email", "password", "is_active",)
