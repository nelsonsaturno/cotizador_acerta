# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0023_solicitudpoliza_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='acreedor',
        ),
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='acreedor_leasing',
        ),
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='leasing',
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='acreedor_leasing_id',
            field=models.IntegerField(default=0, max_length=30, choices=[(0, b'Acreedor'), (1, b'Leasing'), (2, b'Ninguno')]),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='declaracion_prima',
            field=models.CharField(default=b'', max_length=30, choices=[(b'Si', b'Si'), (b'No', b'No')]),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='ilicito',
            field=models.CharField(default=b'', max_length=30, choices=[(b'Si', b'Si'), (b'No', b'No')]),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='politico_expuesto',
            field=models.CharField(default=b'', max_length=30, choices=[(b'Si', b'Si'), (b'No', b'No')]),
        ),
    ]
