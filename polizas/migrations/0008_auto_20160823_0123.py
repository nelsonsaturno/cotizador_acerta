# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0007_extradatoscliente_pais_nacimiento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extradatoscliente',
            old_name='recursos',
            new_name='actividad_principal',
        ),
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='operador',
        ),
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='responsable_pago',
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='ilicito',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='otra_actividad',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='profesion',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='id_conductor',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='id_responsable',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='nombre_conductor',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='nombre_responsable',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='cargo_politico',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='nombre_politico',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='periodo_politico',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='relacion_politico',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.DeleteModel(
            name='Persona',
        ),
    ]
