from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Sistema, Solicitacao


class SolicitacaoForm(ModelForm):

    resumo = forms.CharField(
        label='Resumo',
        max_length=500,
        widget=forms.Textarea)

    class Meta:
        model = Solicitacao
        fields = ['codigo', 'usuario', 'sistema', 'titulo', 'resumo']
        widgets = {'codigo': forms.HiddenInput(),
                   'usuario': forms.HiddenInput()}

    def clean(self):
        import ipdb; ipdb.set_trace()
        if 'usuario' not in self.cleaned_data:
            raise ValidationError("Usuário não definido")


class SolicitacaoEditForm(SolicitacaoForm):

    resumo = forms.CharField(
        label='Resumo',
        max_length=500,
        widget=forms.Textarea)

    class Meta:
        model = Solicitacao
        fields = ['codigo', 'usuario', 'sistema', 'titulo', 'resumo']
        widgets = {'codigo': forms.TextInput(attrs={'readonly': 'readonly'}),
                   'usuario': forms.HiddenInput()}


class SistemaForm(ModelForm):

    class Meta:
        model = Sistema
        fields = ['sigla', 'nome']
