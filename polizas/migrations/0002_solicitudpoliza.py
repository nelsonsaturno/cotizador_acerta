# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0035_marcahistory_modelohistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudPoliza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_conductor', models.CharField(max_length=20)),
                ('id_conductor', models.CharField(max_length=20)),
                ('vigencia_desde', models.DateField()),
                ('vigencia_hasta', models.DateField()),
                ('acreedor', models.CharField(max_length=40)),
                ('leasing', models.CharField(max_length=40)),
                ('opcion', models.CharField(max_length=40)),
                ('firmador', models.CharField(max_length=40)),
                ('observaciones', models.CharField(default=b'', max_length=100)),
                ('responsable', models.CharField(default=b'Contratante', max_length=30, choices=[(b'Contratante', b'Contratante'), (b'Asegurado', b'Asegurado'), (b'Otro', b'Otro')])),
                ('nombre_responsable', models.CharField(max_length=20)),
                ('id_responsable', models.CharField(max_length=20)),
                ('tipo_produccion', models.CharField(default=b'Propia', max_length=30, choices=[(b'Propia', b'Propia'), (b'Coaseguro Lider', b'Coaseguro Lider'), (b'Coaseguro No Lider', b'Coaseguro No Lider'), (b'Reaseguro Cedido', b'Reaseguro Cedido')])),
                ('tipo_suscripcion', models.CharField(default=b'Individual', max_length=30, choices=[(b'Individual', b'Individual'), (b'Colectiva', b'Colectiva')])),
                ('forma_facturacion', models.CharField(default=b'Por Poliza', max_length=30, choices=[(b'Por Poliza', b'Por Poliza'), (b'Por Certificado', b'Por Certificado')])),
                ('renovacion_automatica', models.BooleanField(default=False)),
                ('comision', models.BooleanField(default=False)),
                ('def_comision', models.CharField(max_length=30)),
                ('grupo_economico', models.CharField(max_length=50)),
                ('aprobaciones', models.CharField(max_length=200)),
                ('funcionario', models.CharField(max_length=50)),
                ('cargo_funcionario', models.CharField(max_length=20)),
                ('area_funcionario', models.CharField(default=b'Comercial', max_length=30, choices=[(b'Comercial', b'Comercial'), (b'At. al Cliente', b'At. al Cliente'), (b'Fianzas', b'Fianzas'), (b'Seguros', b'Seguros'), (b'Otro', b'Otro')])),
                ('otra_area', models.CharField(max_length=20)),
                ('cotizacion', models.ForeignKey(to='cotizar.Cotizacion', null=True)),
            ],
        ),
    ]
