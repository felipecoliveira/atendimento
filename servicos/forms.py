from django import forms
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Sistema, Ticket


class TicketForm(ModelForm):

    class Meta:
        model = Ticket
        fields = ['codigo', 'usuario', 'sistema', 'titulo', 'resumo']


class SistemaForm(ModelForm):

    class Meta:
        model = Sistema
        fields = ['sigla', 'nome']
