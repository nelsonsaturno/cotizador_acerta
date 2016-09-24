# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0005_auto_20160918_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='apto',
            field=models.CharField(default=b'', max_length=5),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='cargo_politico',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='edificio',
            field=models.CharField(default=b'', max_length=30),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='ingreso_principal',
            field=models.CharField(default=b'<10,000.00', max_length=30, blank=True, choices=[(b'<10,000.00', b'<10,000.00'), (b'10,000.00-30,000.00', b'10,000.00-30,000.00'), (b'30,000.00-50,000.00', b'30,000.00-50,000.00'), (b'>50,000.00', b'>50,000.00')]),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='no_casa',
            field=models.CharField(default=b'', max_length=5),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='otro_ingreso',
            field=models.CharField(default=b'<10,000.00', max_length=30, blank=True, choices=[(b'<10,000.00', b'<10,000.00'), (b'10,000.00-30,000.00', b'10,000.00-30,000.00'), (b'30,000.00-50,000.00', b'30,000.00-50,000.00'), (b'>50,000.00', b'>50,000.00')]),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='periodo_politico',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='piso',
            field=models.CharField(default=b'', max_length=5),
        ),
    ]
