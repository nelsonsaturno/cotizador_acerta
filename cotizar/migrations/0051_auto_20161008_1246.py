# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0050_auto_20161006_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='tipo_pago',
            field=models.CharField(default=b'Contado', max_length=30, choices=[(b'Contado', b'Contado'), (b'ACH', b'ACH'), (b'Visa', b'Visa'), (b'Otro', b'Otro')]),
        ),
    ]
