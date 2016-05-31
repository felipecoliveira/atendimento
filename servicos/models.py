from django.db import models
from django.utils.translation import ugettext_lazy as _
from usuarios.models import UsuarioExterno


class Servico(models.Model):
    SISTEMA_CHOICES = (
        'DNS',
        'EMAIL',
        'PORTAL MODELO',
        'SAPL',
        'SIGI',
        'SAAP',
        'SPDO',
        )

    usuario = models.ForeignKey(UsuarioExterno)
    titulo = models.CharField(verbose_name=_('Título'), max_length=100)
    descricao = models.models.TextField(verbose_name=_('Descrição'))

    class Meta:
        verbose_name = _('Serviço')
        verbose_name_plural = _('Serviços')

    def __str__(self):
        return self.titulo
