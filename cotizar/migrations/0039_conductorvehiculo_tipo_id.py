# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0038_auto_20160915_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='conductorvehiculo',
            name='tipo_id',
            field=models.CharField(default=b'cedula', max_length=30, null=True, blank=True),
        ),
    ]
