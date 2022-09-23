from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from photo_app.models import Reservations


class LoginForm(forms.Form):
    login = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cd = super().clean()
        login = cd.get('login')
        password = cd.get('password')
        user = authenticate(username=login, password=password)
        if user is None:
            raise ValidationError('Dane logowania nie są prawidłowe')
        self.user = user


class UserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    username = forms.CharField(max_length=60)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean(self):
        cd = super().clean()
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 != password2:
            raise ValidationError('Hasła nie są identyczne.')

    def clean_login(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Wprowadzono błędny login')
        return username


class ReservationsForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = ("date", 'user', 'package', 'phone_number', 'comment', 'status')
