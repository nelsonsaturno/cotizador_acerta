# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0004_auto_20160918_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='conductor',
            field=models.ForeignKey(to='cotizar.ConductorVehiculo', null=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='ref_bancaria',
            field=models.ForeignKey(related_name='bancaria', to='polizas.Referencia', null=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='ref_comercial',
            field=models.ForeignKey(related_name='comercial', to='polizas.Referencia', null=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='ref_personal',
            field=models.ForeignKey(related_name='personal', to='polizas.Referencia', null=True),
        ),
    ]
