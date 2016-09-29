# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0024_auto_20160929_2024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitudpoliza',
            old_name='acreedor_leasing_id',
            new_name='acreedor_leasing',
        ),
    ]
