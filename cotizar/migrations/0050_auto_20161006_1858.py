# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0049_auto_20161006_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='tipo_id',
            field=models.CharField(max_length=30, choices=[(b'Cedula', b'Cedula'), (b'Pasaporte', b'Pasaporte')]),
        ),
    ]
