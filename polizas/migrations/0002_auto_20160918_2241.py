# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='cobrador',
        ),
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='dir_cobro',
        ),
    ]
