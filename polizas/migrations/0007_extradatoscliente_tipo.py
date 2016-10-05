# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0032_tipovehiculo'),
        ('polizas', '0006_auto_20161005_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='extradatoscliente',
            name='tipo',
            field=models.ForeignKey(blank=True, to='administrador.TipoVehiculo', null=True),
        ),
    ]
