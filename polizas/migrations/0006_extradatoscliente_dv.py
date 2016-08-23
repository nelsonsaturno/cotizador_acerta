# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0005_auto_20160815_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='extradatoscliente',
            name='dv',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
