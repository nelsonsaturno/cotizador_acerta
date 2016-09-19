# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0037_auto_20160914_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='fecha_nacimiento',
            field=models.DateField(),
        ),
    ]
