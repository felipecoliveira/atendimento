# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-16 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmaEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('confirmado', models.BooleanField(default=False)),
                ('token', models.CharField(max_length=50, verbose_name='Hash do Email')),
                ('user_id', models.TextField(blank=True, verbose_name='ID do Usuário')),
            ],
            options={
                'verbose_name': 'Email',
                'verbose_name_plural': 'Emails',
            },
        ),
        migrations.AddField(
            model_name='usuario',
            name='email_confirmado',
            field=models.BooleanField(default=False, verbose_name='Email confirmado?'),
        ),
    ]
