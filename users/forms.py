"""User-facing forms for registration, login and profile editing."""

from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


def _validate_github_url(value):
    """Ensure the URL points to github.com."""
    if value and "github.com" not in value.lower():
        raise forms.ValidationError("Ссылка должна вести на github.com")


class UserRegistrationForm(forms.ModelForm):
    """Registration form using model field names directly."""

    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")

    def save(self, commit=True):
        """Create user with username = email."""
        return User.objects.create_user(
            username=self.cleaned_data["email"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            password=self.cleaned_data["password"],
        )


class EmailAuthenticationForm(forms.Form):
    """Authenticate by email + password."""

    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "Введите корректные email и пароль.",
    }

    def __init__(self, request=None, *args, **kwargs):
        """Store request for authenticate()."""
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self):
        """Resolve email to username and authenticate."""
        data = super().clean()
        email = data.get("email", "").lower()
        password = data.get("password")
        if not email or not password:
            return data

        usr = User.objects.filter(email__iexact=email).first()
        username = usr.username if usr else email
        self.user_cache = authenticate(
            self.request,
            username=username,
            password=password,
        )
        if self.user_cache is None:
            raise forms.ValidationError(self.error_messages["invalid_login"])
        return data

    def get_user(self):
        """Return the authenticated user."""
        return self.user_cache


class ProfileEditForm(forms.ModelForm):
    """Edit user profile fields directly on the User model."""

    github = forms.URLField(
        label="GitHub",
        required=False,
        validators=[_validate_github_url],
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "description", "github", "avatar", "phone")
