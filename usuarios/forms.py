import re
from django.core.exceptions import ValidationError
import django_filters

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit, Button
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import EMPTY_VALUES
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import transaction
from .models import Usuario
from captcha.fields import CaptchaField
from datetime import datetime
import crispy_layout_mixin
from crispy_layout_mixin import form_actions
from atendimento.utils import YES_NO_CHOICES


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

    password_confirm = forms.CharField(
        max_length=20,
        label=_('Confirmar Senha'),
        widget=forms.PasswordInput())

    email_confirm = forms.CharField(
        max_length=20,
        label=_('Confirmar Email'))

    captcha = CaptchaField()

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nome_completo', 'password',
                  'password_confirm', 'email_confirm', 'captcha']

    def valida_igualdade(self, texto1, texto2, msg):
        if texto1 != texto2:
            raise ValidationError(msg)
        return True

    def clean(self):

        if ('password' not in self.cleaned_data or
                'password_confirm' not in self.cleaned_data):
            raise ValidationError(_('Favor informar senhas atuais ou novas'))

        msg = _('As senhas não conferem.')
        self.valida_igualdade(
            self.cleaned_data['password'],
            self.cleaned_data['password_confirm'],
            msg)

        if ('email' not in self.cleaned_data or
                'email_confirm' not in self.cleaned_data):
            raise ValidationError(_('Favor informar endereços de email'))

        msg = _('Os emails não conferem.')
        self.valida_igualdade(
            self.cleaned_data['email'],
            self.cleaned_data['email_confirm'],
            msg)

        return self.cleaned_data

    @transaction.atomic
    def save(self, commit=False):
        usuario = super(UsuarioForm, self).save(commit)

        u = User.objects.create(username=usuario.username, email=usuario.email)
        u.set_password(self.cleaned_data['password'])
        u.save()

        usuario.user = u
        usuario.save()
        return usuario


class UsuarioEditForm(UsuarioForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nome_completo', 'password']
        widgets = {'username': forms.TextInput(attrs={'readonly': 'readonly'})}

    def __init__(self, *args, **kwargs):
        super(UsuarioEditForm, self).__init__(*args, **kwargs)
        self.fields['email_confirm'].initial = self.instance.email

    @transaction.atomic
    def save(self, commit=False):
        usuario = super(UsuarioForm, self).save(commit)

        u = usuario.user
        u.email = usuario.email
        u.set_password(self.cleaned_data['password'])
        u.save()

        usuario.data_ultima_atualizacao = datetime.now()
        usuario.save()
        return usuario


class ConveniadoEditForm(ModelForm):
    coveniado = forms.ChoiceField(
        widget=forms.Select(),
        required=True,
        choices=YES_NO_CHOICES)

    class Meta:
        model = Usuario
        fields = ['nome_completo', 'username', 'email', 'conveniado']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'nome_completo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super(ConveniadoEditForm, self).__init__(*args, **kwargs)
        row1 = crispy_layout_mixin.to_row(
            [('username', 4),
             ('nome_completo', 4),
             ('email', 4)])
        row2 = crispy_layout_mixin.to_row([('conveniado', 12)])
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(_('Habilitar'),
                     row1, row2,
                     form_actions(save_label='Conveniado'))
        )


class ResponsavelEditForm(ModelForm):
    responsavel = forms.ChoiceField(
        widget=forms.Select(),
        required=True,
        choices=YES_NO_CHOICES)

    class Meta:
        model = Usuario
        fields = ['nome_completo', 'username', 'email', 'responsavel']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'nome_completo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super(ResponsavelEditForm, self).__init__(*args, **kwargs)
        row1 = crispy_layout_mixin.to_row(
            [('username', 4),
             ('nome_completo', 4),
             ('email', 4)])
        row2 = crispy_layout_mixin.to_row([('responsavel', 12)])
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(_('Habilitar'),
                     row1, row2,
                     form_actions(save_label='Responsável'))
        )
