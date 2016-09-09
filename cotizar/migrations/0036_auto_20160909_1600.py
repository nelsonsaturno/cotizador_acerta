# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cotizar.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0035_marcahistory_modelohistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='anio',
            field=cotizar.models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(1900), django.core.validators.MinValueValidator(2017)]),
        ),
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='historial_transito',
            field=cotizar.models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
    ]
