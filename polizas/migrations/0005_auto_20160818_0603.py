# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0035_marcahistory_modelohistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraDatosCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono_res', models.CharField(max_length=20)),
                ('fax', models.CharField(max_length=20)),
                ('apartado', models.CharField(max_length=100)),
                ('zona', models.CharField(max_length=20)),
                ('motor', models.CharField(max_length=40)),
                ('chasis', models.CharField(max_length=40)),
                ('tipo', models.CharField(max_length=40)),
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
            name='Operador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=20)),
                ('identificacion', models.CharField(max_length=20)),
                ('fecha_nacimiento', models.DateField()),
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
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vigencia_desde', models.DateField()),
                ('vigencia_hasta', models.DateField()),
                ('acreedor', models.CharField(max_length=40)),
                ('opcion', models.CharField(max_length=40)),
                ('agrupador', models.CharField(max_length=40)),
                ('cobrador', models.CharField(max_length=40)),
                ('direccion_cobro', models.CharField(max_length=100)),
                ('cotizacion', models.ForeignKey(to='cotizar.Cotizacion', null=True)),
                ('operador', models.ForeignKey(to='polizas.Operador')),
            ],
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
