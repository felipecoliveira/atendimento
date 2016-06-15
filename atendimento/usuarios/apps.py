from django import apps
from django.utils.translation import ugettext_lazy as _


class AppConfig(apps.AppConfig):
    name = 'atendimento.usuarios'
    verbose_name = _('Usuários')
