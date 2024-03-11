# Authored by Jack Hales, George Piper, James Sadler

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    first_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    last_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    email = forms.CharField(
        widget = forms.EmailInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name', 'password1','password2')

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    email = forms.CharField(
        widget = forms.EmailInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control-file"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')
