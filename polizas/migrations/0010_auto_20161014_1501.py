# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0009_auto_20161008_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='apellido_mat',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='juridico_fecha_constitucion',
            field=models.DateField(default=datetime.date(2016, 10, 14)),
        ),
    ]
