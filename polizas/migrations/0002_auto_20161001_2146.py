# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0032_tipovehiculo'),
        ('polizas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudpoliza',
            name='tipo_acreedor_leasing',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
