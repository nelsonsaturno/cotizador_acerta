# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0008_auto_20160823_0123'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitudpoliza',
            old_name='agrupador',
            new_name='firmador',
        ),
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='cobrador',
        ),
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='direccion_cobro',
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='aprobaciones',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='area_funcionario',
            field=models.CharField(default=b'Comercial', max_length=30, choices=[(b'Comercial', b'Comercial'), (b'At. al Cliente', b'At. al Cliente'), (b'Fianzas', b'Fianzas'), (b'Seguros', b'Seguros'), (b'Otro', b'Otro')]),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='cargo_funcionario',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='comision',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='def_comision',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='forma_facturacion',
            field=models.CharField(default=b'Por Poliza', max_length=30, choices=[(b'Por Poliza', b'Por Poliza'), (b'Por Certificado', b'Por Certificado')]),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='funcionario',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='grupo_economico',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='otra_area',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='renovacion_automatica',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='responsable',
            field=models.CharField(default=b'Contratante', max_length=30, choices=[(b'Contratante', b'Contratante'), (b'Asegurado', b'Asegurado'), (b'Otro', b'Otro')]),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='tipo_produccion',
            field=models.CharField(default=b'Propia', max_length=30, choices=[(b'Propia', b'Propia'), (b'Coaseguro Lider', b'Coaseguro Lider'), (b'Coaseguro No Lider', b'Coaseguro No Lider'), (b'Reaseguro Cedido', b'Reaseguro Cedido')]),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='tipo_suscripcion',
            field=models.CharField(default=b'Individual', max_length=30, choices=[(b'Individual', b'Individual'), (b'Colectiva', b'Colectiva')]),
        ),
    ]
