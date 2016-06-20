from django import forms
from django.db import transaction
from django.forms import ModelForm
from .models import Sistema, Solicitacao

import json, requests

from atendimento.settings import OSTICKET_API_KEY, OSTICKET_URL

def open_osticket(solicitacao):
    headers = {'X-API-KEY': OSTICKET_API_KEY,
               'Content-Type': 'application/json'}

    usuario = solicitacao.usuario
    data = {"alert": True,
            "autorespond": True,
            "source": "API",
            "name": usuario.username,
            "email": usuario.email,
            "phone": '-'.join((usuario.primeiro_telefone.ddd,
                               usuario.primeiro_telefone.numero)),
            "subject": solicitacao.titulo,
            "ip": "",
            "message": solicitacao.resumo}

    response = requests.post(OSTICKET_URL, headers=headers, json=data)
    if response.status_code == requests.codes.ok:
        return response.text
    else:
        response.raise_for_status()

class SolicitacaoForm(ModelForm):

    resumo = forms.CharField(
        label='Resumo',
        max_length=500,
        widget=forms.Textarea)

    class Meta:
        model = Solicitacao
        fields = ['codigo', 'usuario', 'sistema',
                  'email_contato', 'telefone_contato',
                  'casa_legislativa', 'titulo', 'resumo']
        widgets = {'codigo': forms.HiddenInput(),
                   'usuario': forms.HiddenInput()}

    @transaction.atomic
    def save(self, commit=False):
        solicitacao = super(UsuarioForm, self).save(True)
        open_osticket(solicitacao)
        return solicitacao


class SolicitacaoEditForm(ModelForm):

    resumo = forms.CharField(
        label='Resumo',
        max_length=500,
        widget=forms.Textarea)

    class Meta:
        model = Solicitacao
        fields = ['codigo', 'usuario', 'sistema',
                  'casa_legislativa', 'titulo', 'resumo']
        widgets = {'codigo': forms.TextInput(attrs={'readonly': 'readonly'}),
                   'usuario': forms.HiddenInput()}


class SistemaForm(ModelForm):

    class Meta:
        model = Sistema
        fields = ['sigla', 'nome']
