# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extradatoscliente',
            name='conductor',
        ),
        migrations.RemoveField(
            model_name='extradatoscliente',
            name='ref_bancaria',
        ),
        migrations.RemoveField(
            model_name='extradatoscliente',
            name='ref_comercial',
        ),
        migrations.RemoveField(
            model_name='extradatoscliente',
            name='ref_personal',
        ),
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='cotizacion',
        ),
        migrations.DeleteModel(
            name='ExtraDatosCliente',
        ),
        migrations.DeleteModel(
            name='Referencia',
        ),
        migrations.DeleteModel(
            name='SolicitudPoliza',
        ),
    ]
