# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0048_auto_20161006_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='tipo_id',
            field=models.CharField(default='C\xe9dula', max_length=30, choices=[(b'C\xc3\xa9dula', b'C\xc3\xa9dula'), (b'Pasaporte', b'Pasaporte')]),
            preserve_default=False,
        ),
    ]
