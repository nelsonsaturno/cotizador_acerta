# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cotizar', '0034_cotizacion_tipo_pago'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarcaHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='cotizar.Marca')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ModeloHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('marca', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=35)),
                ('descuento', models.FloatField(default=1.0)),
                ('recargo', models.FloatField(default=1.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='cotizar.Modelo')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
