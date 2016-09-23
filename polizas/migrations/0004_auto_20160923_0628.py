# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0003_auto_20160919_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='cargo_politico',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='periodo_politico',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
