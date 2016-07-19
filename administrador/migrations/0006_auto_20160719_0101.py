# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0005_auto_20160711_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historial_transito',
            name='inferior',
            field=models.IntegerField(default=0, unique=True, choices=[(0, 0), (4, 4), (8, 8)]),
        ),
    ]
