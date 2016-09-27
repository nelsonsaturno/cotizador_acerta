# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0011_auto_20160925_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudpoliza',
            name='id_conductor2',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='id_conductor3',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='nombre_conductor2',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='nombre_conductor3',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
