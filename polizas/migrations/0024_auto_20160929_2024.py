# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0031_acreedores'),
        ('polizas', '0023_solicitudpoliza_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='acreedor',
        ),
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='acreedor_leasing',
        ),
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='leasing',
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='acreedor_leasing_id',
            field=models.ForeignKey(default=0, blank=True, to='administrador.Acreedores', null=True),
        ),
    ]
