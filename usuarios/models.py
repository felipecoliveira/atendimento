# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from atendimento.utils import SEXO_CHOICES, UF, YES_NO_CHOICES


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

    class Meta:
        verbose_name = _('Subsecretaria')
        verbose_name_plural = _('Subsecretarias')

    def __str__(self):
        return '[%s] %s' % (self.sigla, self.nome)


class AbstractUsuario(models.Model):

    username = models.CharField(
        verbose_name=_('Nome de Usuário'),
        max_length=50)
    cargo = models.CharField(verbose_name=_('Cargo'), max_length=120)
    nome_completo = models.CharField(
        verbose_name=_('Nome Completo'),
        max_length=128)
    data_criacao = models.DateTimeField(default=timezone.now)
    sexo = models.CharField(
        verbose_name=_('Sexo'),
        max_length=1,
        choices=SEXO_CHOICES,
    )
    cpf = models.CharField(
        verbose_name=_('CPF'),
        max_length=11)
    rg = models.CharField(
        verbose_name=_('RG'),
        max_length=25,
        blank=True,
        null=True)
    email = models.EmailField(
        verbose_name=_('Email'),
        blank=True,
        null=True)
    endereco = models.CharField(verbose_name=_('Endereço'), max_length=256)
    telefone = models.CharField(verbose_name=_('Telefone'), max_length=20)

    class Meta:
        abstract = True


class UsuarioExterno(AbstractUsuario):
    casa_legislativa = models.ManyToManyField(
        CasaLegislativa,
        verbose_name=_('Casa Legislativa'))
    habilitado = models.CharField(
        max_length=3,
        verbose_name=_('Habilitado?'),
        choices=YES_NO_CHOICES)

    class Meta:
        verbose_name = _('Usuário Externo')
        verbose_name_plural = _('Usuários Externo')

    def __str__(self):
        return '%s - Habilitado: %s' % (self.nome_completo, self.habilitado)


class UsuarioInterno(AbstractUsuario):
    matricula = models.CharField(verbose_name=_('Matrícula'), max_length=25)
    subsecretaria = models.ForeignKey(
        Subsecretaria,
        verbose_name=_('Subsecretaria'))

    class Meta:
        verbose_name = _('Usuário Interno')
        verbose_name_plural = _('Usuários Interno')

    def __str__(self):
        return self.nome_completo
