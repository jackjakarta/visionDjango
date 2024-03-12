from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import password_validators_help_text_html, validate_password
# from website.utils.moderation import check_moderate

AuthUser = get_user_model()


class RegisterForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ["first_name", "last_name", "email", "password"]

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=True,
        help_text=password_validators_help_text_html
    )

    password_confirmation = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput,
        required=True,
        help_text="Please confirm your password."
    )

    def save(self, commit=True):
        password = self.cleaned_data["password"]
        self.instance.set_password(password)

        return super().save(commit)
