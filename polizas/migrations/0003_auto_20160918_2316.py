# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0002_auto_20160918_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='banco_tdc',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='expiracion_tdc',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='num_tdc',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='tipo_tdc',
            field=models.CharField(default=b'Visa', max_length=30, null=True, choices=[(b'Visa', b'Visa'), (b'Mastercard', b'Mastercad'), (b'Dinners', b'Dinners'), (b'American Express', b'American Express')]),
        ),
    ]
