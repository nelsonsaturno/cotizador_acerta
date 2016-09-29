# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0012_auto_20160927_2156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extradatoscliente',
            name='estafeta',
        ),
        migrations.RemoveField(
            model_name='extradatoscliente',
            name='fax',
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='acreedor_leasing',
            field=models.CharField(default=b'Ninguno', max_length=30, choices=[(b'Acreedor', b'Acreedor'), (b'Leasing', b'Leasing'), (b'Ninguno', b'Ninguno')]),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='declaracion_prima',
            field=models.CharField(default=b'', max_length=30, blank=True, choices=[(b'Si', b'Si'), (b'No', b'No')]),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='ilicito',
            field=models.CharField(default=b'', max_length=30, blank=True, choices=[(b'Si', b'Si'), (b'No', b'No')]),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='politico_expuesto',
            field=models.CharField(default=b'', max_length=30, blank=True, choices=[(b'Si', b'Si'), (b'No', b'No')]),
        ),
    ]
