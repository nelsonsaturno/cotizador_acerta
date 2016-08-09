# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0018_historialhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialhistory',
            name='inferior',
            field=models.IntegerField(default=0, choices=[(0, 0), (4, 4), (8, 8)]),
        ),
        migrations.AlterField(
            model_name='historialhistory',
            name='superior',
            field=models.IntegerField(default=0, choices=[(3, 3), (7, 7), (10, 10)]),
        ),
    ]
