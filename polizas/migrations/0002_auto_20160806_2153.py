# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0034_cotizacion_tipo_pago'),
        ('polizas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraDatosCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre2', models.CharField(max_length=20)),
                ('apellido_mat', models.CharField(max_length=20)),
                ('apellido_cas', models.CharField(max_length=20)),
                ('nacionalidad', models.CharField(max_length=30)),
                ('residencia', models.CharField(max_length=30)),
                ('profesion', models.CharField(max_length=30)),
                ('ocupacion', models.CharField(max_length=30)),
                ('empresa', models.CharField(max_length=30)),
                ('telefono_emp', models.CharField(max_length=30)),
                ('fax_emp', models.CharField(max_length=30)),
                ('correo_trabajo', models.EmailField(max_length=254)),
                ('politico_expuesto', models.BooleanField(default=False)),
                ('cargo', models.CharField(max_length=30)),
                ('declaracion_prima', models.BooleanField(default=False)),
                ('recursos', models.CharField(max_length=100, blank=True)),
                ('ingreso_principal', models.CharField(default=b'<10,000.00', max_length=30, choices=[(b'<10,000.00', b'<10,000.00'), (b'10,000.00-30,000.00', b'10,000.00-30,000.00'), (b'30,000.00-50,000.00', b'30,000.00-50,000.00'), (b'>50,000.00', b'>50,000.00')])),
                ('otro_ingreso', models.CharField(default=b'<10,000.00', max_length=30, choices=[(b'<10,000.00', b'<10,000.00'), (b'10,000.00-30,000.00', b'10,000.00-30,000.00'), (b'30,000.00-50,000.00', b'30,000.00-50,000.00'), (b'>50,000.00', b'>50,000.00')])),
                ('documento', models.BooleanField(default=False)),
                ('conductor', models.ForeignKey(to='cotizar.ConductorVehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='Referencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=40)),
                ('actividad', models.CharField(max_length=40)),
                ('relacion', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='operador',
            name='conductor',
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='operador',
            field=models.ForeignKey(to='polizas.Operador'),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='ref_bancaria',
            field=models.ForeignKey(related_name='bancaria', to='polizas.Referencia'),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='ref_comercial',
            field=models.ForeignKey(related_name='comercial', to='polizas.Referencia'),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='ref_personal',
            field=models.ForeignKey(related_name='personal', to='polizas.Referencia'),
        ),
    ]
