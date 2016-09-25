# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cotizar.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0036_auto_20160909_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='anio',
            field=cotizar.models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(2017), django.core.validators.MinValueValidator(1900)]),
        ),
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='historial_transito',
            field=cotizar.models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(0)]),
        ),
    ]
