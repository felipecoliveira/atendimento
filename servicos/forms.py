from django import forms
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Sistema, Solicitacao


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

    def clean(self):
        if 'usuario' not in self.cleaned_data:
            raise ValidationError("Usuário não definido")

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
