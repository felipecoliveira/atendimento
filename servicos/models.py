# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from usuarios.models import Usuario


class Sistema(models.Model):
    sigla = models.CharField(verbose_name=_('Sigla'), max_length=10)
    nome = models.CharField(verbose_name=_('Nome Sistema'),
                            max_length=100)
    descricao = models.TextField(null=True,
                                 blank=True,
                                 verbose_name=_('Descrição'))

    class Meta:
        verbose_name = _('Sistema')
        verbose_name_plural = _('Sistemas')

    def __str__(self):
        return "%s - %s" % (sigla, nome)


class Ticket(models.Model):
    codigo = models.PositiveIntegerField()
    usuario = models.ForeignKey(Usuario)
    sistema = models.ForeignKey(Sistema)
    titulo = models.CharField(verbose_name=_('Título'), max_length=100)
    resumo = models.CharField(verbose_name=_('Resumo'), max_length=50)
    data_criacao = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Data de criação'))
    data_fechamento = models.DateTimeField(blank=True,
                                           null=True,
                                           verbose_name=_('Data de criação'))
    descricao = models.TextField(blank=True,
                                 null=True,
                                 verbose_name=_('Descrição'))

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    def __str__(self):
        return "%s - %s" % (numero, resumo)
