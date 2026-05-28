from django import forms
from django.contrib.auth import authenticate, get_user_model

from team_finder.constants import NAME_MAX_LENGTH, SURNAME_MAX_LENGTH

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):

    name = forms.CharField(label='Имя', max_length=NAME_MAX_LENGTH)
    surname = forms.CharField(label='Фамилия', max_length=SURNAME_MAX_LENGTH)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ()

    def save(self, commit=True):
        return User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['name'],
            last_name=self.cleaned_data['surname'],
            password=self.cleaned_data['password'],
        )


class EmailAuthenticationForm(forms.Form):

    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': 'Введите корректные email и пароль.',
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '').lower()
        password = cleaned_data.get('password')
        if not email or not password:
            return cleaned_data

        current_user = User.objects.filter(email__iexact=email).first()
        username = current_user.username if current_user else email
        self.user_cache = authenticate(
            self.request,
            username=username,
            password=password,
        )
        if self.user_cache is None:
            raise forms.ValidationError(self.error_messages['invalid_login'])
        return cleaned_data

    def get_user(self):
        return self.user_cache


class ProfileEditForm(forms.ModelForm):

    name = forms.CharField(label='Имя', max_length=NAME_MAX_LENGTH)
    surname = forms.CharField(label='Фамилия', max_length=SURNAME_MAX_LENGTH)
    about = forms.CharField(label='О себе', required=False, widget=forms.Textarea)
    github_url = forms.URLField(label='GitHub', required=False)

    class Meta:
        model = User
        fields = ('avatar', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_user = self.instance
        if current_user.pk and not self.is_bound:
            self.initial.update({
                'name': current_user.first_name,
                'surname': current_user.last_name,
                'about': current_user.description,
                'phone': current_user.phone,
                'github_url': current_user.github,
            })

    def save(self, commit=True):
        current_user = super().save(commit=False)
        current_user.first_name = self.cleaned_data['name']
        current_user.last_name = self.cleaned_data['surname']
        current_user.description = self.cleaned_data['about']
        current_user.github = self.cleaned_data['github_url']
        if commit:
            current_user.save()
        return current_user
