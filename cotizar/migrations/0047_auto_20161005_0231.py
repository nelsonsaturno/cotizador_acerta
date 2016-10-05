# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0046_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='plan',
            field=models.CharField(default=b'B\xc3\xa1sico', max_length=100),
        ),
    ]
