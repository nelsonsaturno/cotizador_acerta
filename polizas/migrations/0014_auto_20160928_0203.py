# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0013_auto_20160927_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='placa',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
