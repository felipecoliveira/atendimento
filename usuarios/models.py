from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from atendimento.utils import UF


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


class Usuario(models.Model):

    SEXO_CHOICES = (
        ('M', u'Masculino'),
        ('F', u'Feminino'),
    )
    user = models.OneToOneField(User, unique=True)
    nome_completo = models.CharField(max_length=128)
    data_nascimento = models.DateField(
        'Data de Nascimento',
        blank=True,
        null=True,
    )
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        blank=True,
        null=True,
    )
    cpf = models.CharField('CPF', max_length=11, blank=True, null=True)
    rg = models.CharField('RG', max_length=25, blank=True, null=True)
    email = models.EmailField('Email', blank=True, null=True)
    endereco = models.CharField(max_length=256)
    telefone = models.CharField(max_length=15)

    class Meta:
        abstract = True


class Subsecretaria(models.Model):

    nome = models.CharField(max_length=250, null=True)
    sigla = models.CharField(max_length=10, null=True)

    class Meta:
        ordering = ('nome',)

    def __unicode__(self):
        return '%s (%s)' % (self.sigla, self.nome)


class UsuarioExterno(Usuario):
    casa_legislativa = models.ForeignKey(CasaLegislativa)
    homologado = models.BooleanField(default=True)


class UsuarioInterno(Usuario):
    matricula = models.CharField(u'Matrícula',
                                 max_length=25,
                                 blank=True,
                                 null=True)
    subsecretaria = models.ForeignKey(Subsecretaria)
