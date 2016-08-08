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
            name='Operador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=20)),
                ('identificacion', models.CharField(max_length=20)),
                ('fecha_nacimiento', models.DateField()),
                ('conductor', models.ForeignKey(to='cotizar.ConductorVehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono_res', models.CharField(max_length=20)),
                ('fax', models.CharField(max_length=20)),
                ('apartado', models.CharField(max_length=100)),
                ('zona', models.CharField(max_length=20)),
                ('vigencia_desde', models.DateField()),
                ('vigencia_hasta', models.DateField()),
                ('acreedor', models.CharField(max_length=40)),
                ('motor', models.CharField(max_length=40)),
                ('chasis', models.CharField(max_length=40)),
                ('tipo', models.CharField(max_length=40)),
                ('opcion', models.CharField(max_length=40)),
                ('agrupador', models.CharField(max_length=40)),
                ('cobrador', models.CharField(max_length=40)),
                ('direccion_cobro', models.CharField(max_length=100)),
                ('cotizacion', models.ForeignKey(to='cotizar.Cotizacion', null=True)),
                ('operador', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
