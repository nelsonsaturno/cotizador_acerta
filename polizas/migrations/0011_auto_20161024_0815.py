# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0010_auto_20161014_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='juridico_fecha_constitucion',
            field=models.DateField(default=datetime.date(2016, 10, 24)),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='urbanizacion',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
