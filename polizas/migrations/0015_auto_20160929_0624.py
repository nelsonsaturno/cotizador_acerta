# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0014_auto_20160928_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='vigencia_desde',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
