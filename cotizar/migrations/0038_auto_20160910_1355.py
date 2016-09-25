# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0037_auto_20160910_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='edad',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(18)]),
        ),
    ]
