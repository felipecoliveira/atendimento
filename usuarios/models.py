# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from atendimento.utils import UF, YES_NO_CHOICES


class CasaLegislativa(models.Model):
    nome = models.CharField(max_length=100, verbose_name=_('Nome'))
    sigla = models.CharField(max_length=100, verbose_name=_('Sigla'))
    endereco = models.CharField(max_length=100, verbose_name=_('Endereço'))
    cep = models.CharField(max_length=100, verbose_name=_('CEP'))
    municipio = models.CharField(max_length=100, verbose_name=_('Município'))
    uf = models.CharField(max_length=100,
                          choices=UF,
                          verbose_name=_('UF'))
    telefone = models.CharField(
        max_length=100, blank=True, verbose_name=_('Telefone'))
    endereco_web = models.URLField(
        max_length=100, blank=True, verbose_name=_('HomePage'))
    email = models.EmailField(
        max_length=100, blank=True, verbose_name=_('E-mail'))

    class Meta:
        verbose_name = _('Casa Legislativa')
        verbose_name_plural = _('Casas Legislativas')

    def __str__(self):
        return '[%s] %s' % (self.sigla, self.nome)


class Subsecretaria(models.Model):

    nome = models.CharField(verbose_name=_('Nome'), max_length=100, null=True)
    sigla = models.CharField(verbose_name=_('Sigla'), max_length=10, null=True)

    class Meta:
        ordering = ('nome', 'sigla')
        verbose_name = _('Subsecretaria')
        verbose_name_plural = _('Subsecretarias')

    def __str__(self):
        return '[%s] %s' % (self.sigla, self.nome)


class Telefone(models.Model):
    TIPO_TELEFONE = [('FIXO', 'FIXO'), ('CELULAR', 'CELULAR')]

    tipo = models.CharField(
        max_length=7,
        choices=TIPO_TELEFONE,
        verbose_name=_('Tipo Telefone'),)
    ddd = models.CharField(max_length=2, verbose_name=_('DDD'))
    numero = models.CharField(max_length=10, verbose_name=_('Número'))
    principal = models.CharField(
        max_length=10,
        verbose_name=_('Telefone Principal?'),
        choices=YES_NO_CHOICES)

    class Meta:
        verbose_name = _('Telefone')
        verbose_name_plural = _('Telefones')


class Usuario(models.Model):
    '''
        Usuário cadastrado via web
    '''

    TIPO_VINCULO = [('Tercerizado', 'Tercerizado'),
                    ('Efetivo', 'Efetivo'),
                    ('Contratado', 'Contratado')]

    user = models.ForeignKey(User)
    username = models.CharField(
        verbose_name=_('Nome de Usuário'),
        unique=True,
        max_length=50)
    nome_completo = models.CharField(
        verbose_name=_('Nome Completo'),
        max_length=128)
    data_criacao = models.DateTimeField(
        _('Data Criação'),
        default=timezone.now)
    data_ultima_atualizacao = models.DateTimeField(
        default=timezone.now, verbose_name=_('Última atualização'))
    email = models.EmailField(
        unique=True,
        verbose_name=_('Email'))
    habilitado = models.BooleanField(
        default=False,
        verbose_name=_('Habilitado?'))
    conveniado = models.BooleanField(default=False)
    responsavel = models.BooleanField(default=False)
    rg = models.CharField(
        max_length=9,
        null=True,
        verbose_name=_('RG'))
    cpf = models.CharField(
        max_length=11,
        verbose_name=_('CPF'),
        default='00000000000')
    cargo = models.CharField(
        max_length=30,
        verbose_name=_('Cargo'),
        default='--------')
    vinculo = models.CharField(
        max_length=10,
        verbose_name=_('Vinculo'),
        choices=TIPO_VINCULO,
        default='--------')
    casa_legislativa = models.CharField(
        max_length=30,
        verbose_name=_('Casa Legislativa'),
        default='--------')
    primeiro_telefone = models.ForeignKey(
        Telefone, null=True, related_name='primeiro_telefone')
    segundo_telefone = models.ForeignKey(
        Telefone, null=True, related_name='segundo_telefone')

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def __str__(self):
        return self.username
