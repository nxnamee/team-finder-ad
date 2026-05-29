from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'pf-input'})


class SigninForm(AuthenticationForm):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'pf-input'})


class AccountForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio', 'avatar', 'github', 'linkedin', 'website', 'skills', 'role')

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        for f in self.fields.values():
            css = 'pf-input'
            if isinstance(f, forms.ImageField):
                css = 'pf-upload'
            f.widget.attrs.update({'class': css})
