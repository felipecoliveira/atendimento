import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import EMPTY_VALUES
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import transaction
from .models import Usuario


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username", max_length=30,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'username'}))

    password = forms.CharField(
        label="Password", max_length=30,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'name': 'password'}))


class UsuarioForm(ModelForm):
    password = forms.CharField(
        max_length=20,
        label=_('Senha'),
        widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nome_completo', 'password']

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #
    #     return email

    @transaction.atomic
    def save(self, commit=False):
        usuario = super(UsuarioForm, self).save(commit)

        u = User()
        u.username = usuario.username
        u.set_password(self.cleaned_data['password'])
        u.email = usuario.email
        u.save()

        usuario.user = u
        usuario.save()
        return usuario
