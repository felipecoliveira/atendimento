# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-02 12:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0004_auto_20160602_0947'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0005_auto_20160601_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, verbose_name='Nome de Usuário')),
                ('password', models.CharField(max_length=20, verbose_name='Senha')),
                ('nome_completo', models.CharField(max_length=128, verbose_name='Nome Completo')),
                ('data_criacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_ultima_atualizacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('habilitado', models.CharField(choices=[(True, 'Sim'), (False, 'Não')], default='Sim', max_length=3, verbose_name='Habilitado?')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
        ),
        migrations.RemoveField(
            model_name='usuarioexterno',
            name='casa_legislativa',
        ),
        migrations.DeleteModel(
            name='UsuarioExterno',
        ),
    ]
