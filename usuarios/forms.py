import re
from datetime import datetime

from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Fieldset, Layout, Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES, validate_email
from django.db import transaction
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _

import crispy_layout_mixin
from atendimento.utils import YES_NO_CHOICES
from crispy_layout_mixin import form_actions

from .models import Telefone, Usuario


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
    # Telefone
    TIPO_TELEFONE = [('FIXO', 'FIXO'), ('CELULAR', 'CELULAR')]

    # Primeiro Telefone
    primeiro_tipo = forms.ChoiceField(
        widget=forms.Select(),
        choices=TIPO_TELEFONE,
        label=_('Tipo Telefone'))
    primeiro_ddd = forms.CharField(max_length=2, label=_('DDD'))
    primeiro_numero = forms.CharField(max_length=10, label=_('Número'))
    primeiro_principal = forms.TypedChoiceField(
        widget=forms.Select(),
        label=_('Telefone Principal?'),
        choices=YES_NO_CHOICES)

    # Primeiro Telefone
    segundo_tipo = forms.ChoiceField(
        required=False,
        widget=forms.Select(),
        choices=TIPO_TELEFONE,
        label=_('Tipo Telefone'))
    segundo_ddd = forms.CharField(required=False, max_length=2, label=_('DDD'))
    segundo_numero = forms.CharField(
        required=False, max_length=10, label=_('Número'))
    segundo_principal = forms.ChoiceField(
        required=False,
        widget=forms.Select(),
        label=_('Telefone Principal?'),
        choices=YES_NO_CHOICES)

    # Usuário
    password = forms.CharField(
        max_length=20,
        label=_('Senha'),
        widget=forms.PasswordInput())

    password_confirm = forms.CharField(
        max_length=20,
        label=_('Confirmar Senha'),
        widget=forms.PasswordInput())

    email_confirm = forms.EmailField(
        required=True,
        label=_('Confirmar Email'))

    captcha = CaptchaField()

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nome_completo', 'password', 'vinculo',
                  'password_confirm', 'email_confirm', 'captcha', 'cpf', 'rg',
                  'cargo', 'casa_legislativa']

    def valida_igualdade(self, texto1, texto2, msg):
        if texto1 != texto2:
            raise ValidationError(msg)
        return True

    def clean_primeiro_numero(self):
        cleaned_data = self.cleaned_data

        telefone = Telefone()
        telefone.tipo = self.data['primeiro_tipo']
        telefone.ddd = self.data['primeiro_ddd']
        telefone.numero = self.data['primeiro_numero']
        telefone.principal = self.data['primeiro_principal']

        cleaned_data['primeiro_telefone'] = telefone
        return cleaned_data

    def clean_segundo_numero(self):
        cleaned_data = self.cleaned_data

        telefone = Telefone()
        telefone.tipo = self.data['segundo_tipo']
        telefone.ddd = self.data['segundo_ddd']
        telefone.numero = self.data['segundo_numero']
        telefone.principal = self.data['segundo_principal']

        cleaned_data['segundo_telefone'] = telefone
        return cleaned_data

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

        email_existente = Usuario.objects.filter(
            email=self.cleaned_data['email'])

        if email_existente:
            msg = _('Esse email já foi cadastrado.')
            raise ValidationError(msg)

        return self.cleaned_data

    @transaction.atomic
    def save(self, commit=False):
        usuario = super(UsuarioForm, self).save(commit)

        # Cria telefones
        tel = Telefone.objects.create(
            tipo=self.data['primeiro_tipo'],
            ddd=self.data['primeiro_ddd'],
            numero=self.data['primeiro_numero'],
            principal=self.data['primeiro_principal']
        )
        usuario.primeiro_telefone = tel

        tel = self.cleaned_data['segundo_telefone']
        if (tel.tipo and tel.ddd and tel.numero and tel.principal):
            tel = Telefone.objects.create(
                tipo=self.data['segundo_tipo'],
                ddd=self.data['segundo_ddd'],
                numero=self.data['segundo_numero'],
                principal=self.data['segundo_principal']
            )
            usuario.segundo_telefone = tel

        # Cria User
        u = User.objects.create(username=usuario.username, email=usuario.email)
        u.set_password(self.cleaned_data['password'])
        u.save()

        usuario.user = u
        usuario.save()
        return usuario


class UsuarioEditForm(UsuarioForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nome_completo', 'password', 'vinculo',
                  'password_confirm', 'email_confirm', 'captcha', 'cpf', 'rg',
                  'cargo', 'casa_legislativa']
        widgets = {'username': forms.TextInput(attrs={'readonly': 'readonly'})}

    def __init__(self, *args, **kwargs):
        super(UsuarioEditForm, self).__init__(*args, **kwargs)
        self.fields['email_confirm'].initial = self.instance.email

    @transaction.atomic
    def save(self, commit=False):
        usuario = super(UsuarioForm, self).save(commit)

        # Primeiro telefone
        tel = usuario.primeiro_telefone

        tel.tipo = self.data['primeiro_tipo']
        tel.ddd = self.data['primeiro_ddd']
        tel.numero = self.data['primeiro_numero']
        tel.principal = self.data['primeiro_principal']
        tel.save()

        usuario.primeiro_telefone = tel

        # Segundo telefone
        tel = usuario.segundo_telefone

        if tel:
            tel.tipo = self.data['segundo_tipo']
            tel.ddd = self.data['segundo_ddd']
            tel.numero = self.data['segundo_numero']
            tel.principal = self.data['segundo_principal']
            tel.save()
            usuario.segundo_telefone = tel

        tel = self.cleaned_data['segundo_telefone']
        if (tel.tipo and tel.ddd and tel.numero and tel.principal):
            tel = Telefone.objects.create(
                tipo=self.data['segundo_tipo'],
                ddd=self.data['segundo_ddd'],
                numero=self.data['segundo_numero'],
                principal=self.data['segundo_principal']
            )
            usuario.segundo_telefone = tel

        # User
        u = usuario.user
        u.email = usuario.email
        u.set_password(self.cleaned_data['password'])
        u.save()

        usuario.data_ultima_atualizacao = datetime.now()
        usuario.save()
        return usuario


class HabilitarEditForm(ModelForm):
    habilitado = forms.ChoiceField(
        widget=forms.Select(),
        required=True,
        choices=YES_NO_CHOICES)

    class Meta:
        model = Usuario
        fields = ['nome_completo', 'username', 'email', 'habilitado']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'nome_completo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super(HabilitarEditForm, self).__init__(*args, **kwargs)
        row1 = crispy_layout_mixin.to_row(
            [('username', 4),
             ('nome_completo', 4),
             ('email', 4)])
        row2 = crispy_layout_mixin.to_row([('habilitado', 12)])
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(_('Editar usuário'),
                     row1, row2,
                     form_actions(more=[Submit('Cancelar', 'Cancelar', style='background-color:black; color:white;')]))
        )
