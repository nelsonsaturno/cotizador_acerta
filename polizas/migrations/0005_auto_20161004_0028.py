# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0004_auto_20161003_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='juridico_fecha_constitucion',
            field=models.DateField(default=datetime.date(2016, 10, 4)),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='asegurado',
            field=models.CharField(max_length=100),
        ),
    ]
