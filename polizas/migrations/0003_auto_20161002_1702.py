# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0002_auto_20161001_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='juridico_fecha_constitucion',
            field=models.DateField(default=datetime.date(2016, 10, 2)),
        ),
    ]
