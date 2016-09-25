# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0008_auto_20160925_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='tipo_tdc',
            field=models.CharField(default=b'Visa', max_length=30, null=True, choices=[(b'Visa', b'Visa'), (b'Mastercard', b'Mastercad')]),
        ),
    ]
