# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0017_auto_20160928_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='aprobaciones',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='area_funcionario',
            field=models.CharField(default=b'Comercial', max_length=30, blank=True, choices=[(b'Comercial', b'Comercial'), (b'At. al Cliente', b'At. al Cliente'), (b'Fianzas', b'Fianzas'), (b'Seguros', b'Seguros'), (b'Otro', b'Otro')]),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='cargo_funcionario',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='def_comision',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='forma_facturacion',
            field=models.CharField(default=b'Por Poliza', max_length=30, blank=True, choices=[(b'Por Poliza', b'Por Poliza'), (b'Por Certificado', b'Por Certificado')]),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='funcionario',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='grupo_economico',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='otra_area',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='tipo_produccion',
            field=models.CharField(default=b'Propia', max_length=30, blank=True, choices=[(b'Propia', b'Propia'), (b'Coaseguro Lider', b'Coaseguro Lider'), (b'Coaseguro No Lider', b'Coaseguro No Lider'), (b'Reaseguro Cedido', b'Reaseguro Cedido')]),
        ),
        migrations.AlterField(
            model_name='solicitudpoliza',
            name='tipo_suscripcion',
            field=models.CharField(default=b'Individual', max_length=30, blank=True, choices=[(b'Individual', b'Individual'), (b'Colectiva', b'Colectiva')]),
        ),
    ]
