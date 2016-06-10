# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-10 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0007_solicitacao_casa_legislativa'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacao',
            name='email_contato',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email de contato'),
        ),
        migrations.AddField(
            model_name='solicitacao',
            name='telefone_contato',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone de contato'),
        ),
    ]
