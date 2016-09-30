# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0032_tipovehiculo'),
        ('polizas', '0026_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='acreedor_leasing_id',
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='acreedor_leasing',
            field=models.ForeignKey(default=0, blank=True, to='administrador.Acreedores', null=True),
        ),
    ]
