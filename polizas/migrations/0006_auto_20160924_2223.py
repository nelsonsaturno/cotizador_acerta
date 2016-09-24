# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0005_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='num_tdc',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
