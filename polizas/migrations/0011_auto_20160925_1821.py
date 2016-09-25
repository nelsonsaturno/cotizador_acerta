# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0010_solicitudpoliza_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='conductor',
            field=models.ForeignKey(related_name='datos', to='cotizar.ConductorVehiculo', null=True),
        ),
    ]
