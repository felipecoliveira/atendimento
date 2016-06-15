from datetime import datetime

from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit
from django import forms
from django.conf import settings
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
# from django.core.mail import send_mail
from django.db import transaction
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

import atendimento.crispy_layout_mixin
from atendimento.utils import YES_NO_CHOICES
from atendimento.crispy_layout_mixin import form_actions

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
        widget=forms.TextInput(attrs={'style': 'text-transform:lowercase;'}),
        label=_('Confirmar Email'))

    captcha = CaptchaField()

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nome_completo', 'password', 'vinculo',
                  'password_confirm', 'email_confirm', 'captcha', 'cpf', 'rg',
                  'cargo', 'casa_legislativa']

        widgets = {'email': forms.TextInput(
                               attrs={'style': 'text-transform:lowercase;'}),}

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['rg'].widget.attrs['class'] = 'rg'
        self.fields['cpf'].widget.attrs['class'] = 'cpf'
        self.fields['primeiro_numero'].widget.attrs['class'] = 'telefone'
        self.fields['primeiro_ddd'].widget.attrs['class'] = 'ddd'
        self.fields['segundo_numero'].widget.attrs['class'] = 'telefone'
        self.fields['segundo_ddd'].widget.attrs['class'] = 'ddd'

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

    def valida_email_existente(self):
        return Usuario.objects.filter(
                email=self.cleaned_data['email']).exists()

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

        email_existente = self.valida_email_existente()

        if email_existente:
            msg = _('Esse email já foi cadastrado.')
            raise ValidationError(msg)
        # import ipdb; ipdb.set_trace()

        try:
            validate_password(self.cleaned_data['password'])
        except ValidationError as error:
            raise ValidationError(error)

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

        # assunto = "Cadastro no Sistema de Atendimento ao Usuário"
        # mensagem = ("Este e-mail foi utilizado para fazer cadastro no " +
        #             "Sistema de Atendimento ao Usuário do Interlegis.\n" +
        #             "Caso você não tenha feito este cadastro, por favor " +
        #             "ignore esta mensagem.")
        # remetente = settings.EMAIL_HOST_USER
        # destinatario = [usuario.email,
        #                 settings.EMAIL_HOST_USER]
        # send_mail(assunto, mensagem, remetente, destinatario,
        #           fail_silently=False)

        u.save()

        usuario.user = u
        usuario.save()


class UsuarioEditForm(UsuarioForm):

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nome_completo', 'vinculo',
                  'email_confirm', 'captcha', 'cpf', 'rg',
                  'cargo', 'casa_legislativa']
        widgets = {'username': forms.TextInput(attrs={'readonly': 'readonly'}),
                  'email': forms.TextInput(
                                 attrs={'style': 'text-transform:lowercase;'}),
                  }

    def __init__(self, *args, **kwargs):
        super(UsuarioEditForm, self).__init__(*args, **kwargs)
        self.fields['email_confirm'].initial = self.instance.email
        self.fields.pop('password')
        self.fields.pop('password_confirm')

    def valida_email_existente(self):
        '''Não permite atualizar emails para
           emails existentes de outro usuário
        '''
        return Usuario.objects.filter(
                    email=self.cleaned_data['email']).exclude(
                    user__username=self.cleaned_data['username']).exists()

    def clean(self):

        if ('email' not in self.cleaned_data or
                'email_confirm' not in self.cleaned_data):
            raise ValidationError(_('Favor informar endereços de email'))

        msg = _('Os emails não conferem.')
        self.valida_igualdade(
            self.cleaned_data['email'],
            self.cleaned_data['email_confirm'],
            msg)

        email_existente = self.valida_email_existente()

        if email_existente:
            msg = _('Esse email já foi cadastrado.')
            raise ValidationError(msg)

        return self.cleaned_data

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
        fields = ['cpf', 'nome_completo', 'email', 'habilitado']
        widgets = {
            'cpf': forms.TextInput(attrs={'readonly': 'readonly'}),
            'nome_completo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super(HabilitarEditForm, self).__init__(*args, **kwargs)
        row1 = crispy_layout_mixin.to_row(
            [('nome_completo', 4),
             ('cpf', 4),
             ('email', 4)])
        row2 = crispy_layout_mixin.to_row([('habilitado', 12)])
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(_('Editar usuário'),
                     row1, row2,
                     form_actions(
                        more=[
                            Submit(
                                'Cancelar',
                                'Cancelar',
                                style='background-color:black; color:white;')])
                     )
        )


class MudarSenhaForm(ModelForm):

    password = forms.CharField(
        max_length=20,
        label=_('Nova Senha'),
        widget=forms.PasswordInput())

    password_confirm = forms.CharField(
        max_length=20,
        label=_('Confirmar Nova Senha'),
        widget=forms.PasswordInput())

    captcha = CaptchaField()

    def valida_igualdade(self, texto1, texto2, msg):
        if texto1 != texto2:
            raise ValidationError(msg)
        return True

    def clean(self):
        if ('password' not in self.cleaned_data or
                'password_confirm' not in self.cleaned_data):
            raise ValidationError(_('Favor informar senhas atuais \
                                     ou novas'))

        msg = _('As senhas não conferem.')
        self.valida_igualdade(
            self.cleaned_data['password'],
            self.cleaned_data['password_confirm'],
            msg)

        try:
            validate_password(self.cleaned_data['password'])
        except ValidationError as error:
            raise ValidationError(error)

    class Meta:
        model = Usuario
        fields = ['password', 'password_confirm', 'captcha']

    def __init__(self, *args, **kwargs):
        super(MudarSenhaForm, self).__init__(*args, **kwargs)
        row1 = crispy_layout_mixin.to_row(
            [('password', 6),
             ('password_confirm', 6)])
        row2 = crispy_layout_mixin.to_row([('captcha', 12)])
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(_('Mudar Senha'),
                     row1, row2,
                     form_actions(
                        more=[
                            Submit(
                                'Cancelar',
                                'Cancelar',
                                style='background-color:black; color:white;')])
                     )
        )


class RecuperarSenhaEmailForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(RecuperarSenhaEmailForm, self).__init__(*args, **kwargs)
        row1 = crispy_layout_mixin.to_row(
            [('email', 6)])
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(_('Recuperar Senha'),
                     row1,
                     form_actions(
                        more=[
                            Submit(
                                'Cancelar',
                                'Cancelar',
                                style='background-color:black; color:white;')])
                     )
        )

    def clean(self):
        email_existente_usuario = Usuario.objects.filter(
            email=self.cleaned_data['email'])
        email_existente_user = User.objects.filter(
            email=self.cleaned_data['email'])

        if not email_existente_usuario and not email_existente_user:
            msg = _('Não existe nenhum usuário cadastrado com este e-mail.')
            raise ValidationError(msg)

        return self.cleaned_data


class RecuperacaoMudarSenhaForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(RecuperacaoMudarSenhaForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''
        row1 = crispy_layout_mixin.to_row(
            [('new_password1', 6),
             ('new_password2', 6)])
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(_(''),
                     row1,
                     form_actions(
                        more=[
                            Submit(
                                'Cancelar',
                                'Cancelar',
                                style='background-color:black; color:white;')])
                     )
        )
