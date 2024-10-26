from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import (
    password_validators_help_text_html,
    validate_password,
)

# from website.utils.moderation import check_moderate

AuthUser = get_user_model()


class RegisterForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = [
            "first_name",
            "last_name",
            "email",
        ]


class PasswordForm(forms.Form):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Set Password"}
        ),
        required=True,
        help_text=password_validators_help_text_html,
    )

    password_confirmation = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
        required=True,
        help_text="Please confirm your password.",
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)

        return password

    def clean_password_confirmation(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")

        if not password == password_confirmation:
            raise forms.ValidationError("Password not confirmed!")

        return password

    def save(self):
        password = self.cleaned_data.get("password")
        self.user.set_password(password)
        self.user.save()
