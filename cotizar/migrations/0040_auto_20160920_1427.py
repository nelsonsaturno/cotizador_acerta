# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0039_conductorvehiculo_tipo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='historial_transito',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(0)]),
        ),
    ]
