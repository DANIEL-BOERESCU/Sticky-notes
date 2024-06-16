# accounts/forms.py

from django import forms

from app.models import *

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import AuthenticationForm


# Code for the Register form class
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    # Form fields
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {
            "username": None,
            "password1": None,
            "password2": None,
        }

    # Code for handling wrong password inputs
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        errors = []

        if password1 != password2:
            errors.append(forms.ValidationError("The passwords do not match."))
        if len(password1) < 8:
            errors.append(
                forms.ValidationError(
                    "The password must be at least 8 characters long."
                )
            )
        if not any(char.isdigit() for char in password1):
            errors.append(
                forms.ValidationError("The password must contain at least one digit.")
            )

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data

    # Code for handling wrong username inputs
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken. Please choose a different one."
            )
        return username

    # Code for handling wrong user email inputs
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already in use. Please use a different email address."
            )
        return email


# Code to handle inactive accounts.
class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.",
                code="inactive",
            )
