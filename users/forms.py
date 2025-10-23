from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username")


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating Custom User model.
    """
    class Meta:
        model = User
        fields = (
            # Personal info
            "profile_pic",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "date_of_birth",
            "country",
            "bio",
            # Authentication / permissions
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
        )