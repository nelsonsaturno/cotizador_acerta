# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0032_tipovehiculo'),
        ('polizas', '0028_remove_extradatoscliente_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='extradatoscliente',
            name='tipo',
            field=models.ForeignKey(blank=True, to='administrador.TipoVehiculo', null=True),
        ),
    ]
