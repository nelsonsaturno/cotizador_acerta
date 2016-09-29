# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0023_solicitudpoliza_num'),
    ]

    operations = [
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
