import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import EMPTY_VALUES
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import UsuarioExterno


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username", max_length=30,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'username'}))

    password = forms.CharField(
        label="Password", max_length=30,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'name': 'password'}))


def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0


class UsuarioExternoForm(ModelForm):

    class Meta:
        model = UsuarioExterno
        fields = ['username', 'email', 'cargo', 'nome_completo', 'sexo',
                  'cpf', 'rg', 'endereco', 'telefone', 'casa_legislativa']

    default_error_messages = {
            'invalid': _("CPF Inválido."),
            'digits_only': _("Este campo só aceita números."),
            'max_digits': _('Este campo requer 11 digitos.'),
    }

    def validate_CPF(self, value):

        if value in EMPTY_VALUES:
            return u''

        if not value.isdigit():
            value = re.sub("[-\.]", "", value)
        orig_value = value[:]

        try:
            int(value)
        except ValueError:
            raise ValidationError(self.error_messages['digits_only'])

        if len(value) != 11:
            raise ValidationError(self.error_messages['max_digits'])
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(
            range(10, 1, -1))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(
            range(11, 1, -1))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)

        if value[-2:] != orig_dv:
            raise ValidationError(self.error_messages['invalid'])

        return orig_value

    def clean_cpf(self):
        return self.validate_CPF(self.cleaned_data['cpf'])

    def save(self, commit=False):
        usuario = super(UsuarioExternoForm, self).save(commit)
        usuario.habilitado = False
        usuario.save()
        return usuario
