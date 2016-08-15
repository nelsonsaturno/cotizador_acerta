# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0035_marcahistory_modelohistory'),
        ('polizas', '0004_auto_20160815_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudPoliza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vigencia_desde', models.DateField()),
                ('vigencia_hasta', models.DateField()),
                ('acreedor', models.CharField(max_length=40)),
                ('leasing', models.CharField(max_length=40)),
                ('opcion', models.CharField(max_length=40)),
                ('agrupador', models.CharField(max_length=40)),
                ('cobrador', models.CharField(max_length=40)),
                ('direccion_cobro', models.CharField(max_length=100)),
                ('observaciones', models.CharField(default=b'', max_length=100)),
                ('cotizacion', models.ForeignKey(to='cotizar.Cotizacion', null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Operador',
            new_name='Persona',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='cotizacion',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='operador',
        ),
        migrations.RemoveField(
            model_name='extradatoscliente',
            name='apartado',
        ),
        migrations.RemoveField(
            model_name='extradatoscliente',
            name='zona',
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='placa',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Solicitud',
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='operador',
            field=models.ForeignKey(related_name='Operador', to='polizas.Persona'),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='responsable_pago',
            field=models.ForeignKey(related_name='Responsable', to='polizas.Persona', null=True),
        ),
    ]
