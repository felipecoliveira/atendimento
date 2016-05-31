from django.db import models


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

    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=200)
