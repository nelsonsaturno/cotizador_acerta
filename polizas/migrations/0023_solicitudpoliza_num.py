# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0022_auto_20160929_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudpoliza',
            name='num',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
