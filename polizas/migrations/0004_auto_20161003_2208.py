# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0032_tipovehiculo'),
        ('polizas', '0003_auto_20161002_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='extradatoscliente',
            name='tipo',
            field=models.ForeignKey(blank=True, to='administrador.TipoVehiculo', null=True),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='asegurado',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='id_asegurado',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='juridico_fecha_constitucion',
            field=models.DateField(default=datetime.date(2016, 10, 3)),
        ),
    ]
