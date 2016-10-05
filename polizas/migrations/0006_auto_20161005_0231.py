# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0005_auto_20161004_0028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extradatoscliente',
            name='tipo',
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='juridico_fecha_constitucion',
            field=models.DateField(default=datetime.date(2016, 10, 5)),
        ),
    ]
