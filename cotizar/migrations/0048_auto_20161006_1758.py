# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0047_auto_20161005_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conductorvehiculo',
            name='tipo_id',
            field=models.CharField(blank=True, max_length=30, null=True, choices=[(b'C\xc3\xa9dula', b'C\xc3\xa9dula'), (b'Pasaporte', b'Pasaporte')]),
        ),
    ]
