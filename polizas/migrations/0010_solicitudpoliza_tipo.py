# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0009_auto_20160925_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudpoliza',
            name='tipo',
            field=models.CharField(default=b'Solicitada', max_length=30, choices=[(b'Solicitada', b'Solicitada'), (b'Emitida', b'Emitida')]),
        ),
    ]
