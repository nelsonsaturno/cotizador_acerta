# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0043_conductorvehiculo_tipo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='tipo_id',
            field=models.CharField(blank=True, max_length=30, null=True, choices=[(0, b'C\xc3\xa9dula'), (1, b'Pasaporte')]),
        ),
    ]