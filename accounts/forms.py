from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if not email:
            raise forms.ValidationError(
                'Email обязателен'
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        first_name = cleaned_data.get(
            'first_name'
        )

        last_name = cleaned_data.get(
            'last_name'
        )

        if not first_name and not last_name:
            raise forms.ValidationError(
                'Заполните имя или фамилию'
            )

        return cleaned_data