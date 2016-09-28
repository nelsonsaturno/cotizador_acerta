# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0016_auto_20160929_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='vigencia_desde',
            field=models.DateField(),
        ),
    ]
