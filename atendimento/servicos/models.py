# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from atendimento.usuarios.models import Usuario


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
        return "%s - %s" % (self.sigla, self.nome)


class Solicitacao(models.Model):
    codigo = models.PositiveIntegerField(unique=True)
    usuario = models.ForeignKey(Usuario)
    sistema = models.ForeignKey(Sistema)
    titulo = models.CharField(verbose_name=_('Título'), max_length=100)
    resumo = models.CharField(verbose_name=_('Resumo'), max_length=50)
    casa_legislativa = models.CharField(verbose_name=_('Casa Legislativa'),
                                        max_length=200)
    email_contato = models.EmailField(blank=True,
                                      null=True,
                                      verbose_name=_('Email de contato'))
    # Substituir por usuarios.models.Telefone?
    telefone_contato = models.CharField(max_length=15,
                                        null=True,
                                        blank=True,
                                        verbose_name=_('Telefone de contato'))

    data_criacao = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Data de criação'))
    descricao = models.TextField(blank=True,
                                 null=True,
                                 verbose_name=_('Descrição'))

    class Meta:
        verbose_name = _('Solicitação de Novo Serviço')
        verbose_name_plural = _('Solicitações de Novos Serviços')
        ordering = ['data_criacao']

    def __str__(self):
        return "%s - %s" % (self.codigo, self.resumo)
