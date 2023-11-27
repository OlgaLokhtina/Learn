from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class ProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'username'}))
    last_name = forms.CharField#(widget=forms.TextInput(attrs={
        #'class': 'last_name'}))
    first_name = forms.CharField#(widget=forms.TextInput(attrs={
      #  'class': 'first_name'}))
    email = forms.CharField#(widget=forms.TextInput(attrs={
        #'class': 'email'}))
    country = forms.ChoiceField
    city = forms.ChoiceField
    class Meta:
        model = User
        fields = ["username", "last_name", "first_name", "email", "country", "city"]



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-login', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-password', 'placeholder': 'Введите пароль'}))
    class Meta:
        model = User
        fields = ["username", "password"]