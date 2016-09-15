# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0036_auto_20160829_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='fecha_nacimiento',
            field=models.DateField(auto_now_add=True),
        ),
    ]
