# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='cotizacion',
        ),
        migrations.DeleteModel(
            name='SolicitudPoliza',
        ),
    ]
