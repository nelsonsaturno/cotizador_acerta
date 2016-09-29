# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0019_auto_20160928_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='actividad_empresa',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='cargo_empresa',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='direccion_empresa',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='empresa',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='fax_empresa',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='ocupacion',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='profesion',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
