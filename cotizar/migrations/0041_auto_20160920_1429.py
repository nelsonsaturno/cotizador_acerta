# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0040_auto_20160920_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conductorvehiculo',
            name='tipo_id',
        ),
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='historial_transito',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
    ]
