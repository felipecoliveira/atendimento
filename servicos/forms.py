from django import forms
from django.forms import ModelForm

from .models import Sistema, Solicitacao


class SolicitacaoForm(ModelForm):

    resumo = forms.CharField(
        label='Resumo',
        max_length=500,
        widget=forms.Textarea)

    class Meta:
        model = Solicitacao
        fields = ['codigo', 'usuario', 'sistema',
                  'casa_legislativa', 'titulo', 'resumo']
        widgets = {'codigo': forms.HiddenInput(),
                   'usuario': forms.HiddenInput()}


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
