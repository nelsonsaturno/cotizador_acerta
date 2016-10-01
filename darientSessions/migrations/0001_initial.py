# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CorredorVendedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('corredor', models.ForeignKey(related_name='corredor', to=settings.AUTH_USER_MODEL)),
                ('vendedor', models.ForeignKey(related_name='vendedor', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name_plural': 'CorredorVendedors',
            },
        ),
        migrations.CreateModel(
            name='DatosCorredor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ruc', models.CharField(max_length=100)),
                ('licencia', models.CharField(max_length=100)),
                ('razon_social', models.CharField(max_length=100, null=True, blank=True)),
                ('planes', models.CharField(default=b'-', max_length=100, choices=[(b'Plan 1', b'Plan 1'), (b'Plan 2', b'Plan 2'), (b'Plan 3', b'Plan 3')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PolizasCorredor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('polizas_desde', models.PositiveIntegerField(default=1)),
                ('polizas_hasta', models.PositiveIntegerField(default=50000)),
                ('polizas', models.IntegerField(default=0)),
                ('user', models.OneToOneField(related_name='polizas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, blank=True)),
                ('key_expires', models.DateTimeField(default=datetime.date(2016, 10, 1))),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User profiles',
            },
        ),
    ]
