# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-06 13:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import usuarios.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        ('usuarios', '0016_auto_20160603_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='grupo_usuario',
            field=models.ForeignKey(default=usuarios.models.grupo_usuario_comum, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
