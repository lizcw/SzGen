from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms import Form, ModelForm, DateInput
from captcha.fields import CaptchaField
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}),
                   'password': forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'})
                   }


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control', 'name': 'email'})
                   }


class AxesCaptchaForm(Form):
    captcha = CaptchaField()
