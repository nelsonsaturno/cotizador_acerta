# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0035_marcahistory_modelohistory'),
        ('polizas', '0002_solicitudpoliza'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraDatosCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('placa', models.CharField(max_length=40)),
                ('motor', models.CharField(max_length=40)),
                ('chasis', models.CharField(max_length=40)),
                ('tipo', models.CharField(max_length=40)),
                ('nombre2', models.CharField(max_length=20)),
                ('apellido_mat', models.CharField(max_length=20)),
                ('apellido_cas', models.CharField(max_length=20)),
                ('dv', models.CharField(max_length=20)),
                ('nacionalidad', models.CharField(max_length=30)),
                ('pais_nacimiento', models.CharField(max_length=30)),
                ('pais_residencia', models.CharField(max_length=30)),
                ('provincia', models.CharField(max_length=30)),
                ('distrito', models.CharField(max_length=30)),
                ('corregimiento', models.CharField(max_length=30)),
                ('urbanizacion', models.CharField(max_length=30)),
                ('edificio', models.CharField(default=b'N/A', max_length=30)),
                ('piso', models.CharField(default=b'N/A', max_length=5)),
                ('apto', models.CharField(default=b'N/A', max_length=5)),
                ('calle_ave', models.CharField(max_length=30)),
                ('no_casa', models.CharField(default=b'N/A', max_length=5)),
                ('apartado_postal', models.CharField(max_length=30)),
                ('telefono_res', models.CharField(max_length=20)),
                ('fax', models.CharField(max_length=20)),
                ('estafeta', models.CharField(max_length=30)),
                ('profesion', models.CharField(max_length=30)),
                ('ocupacion', models.CharField(max_length=30)),
                ('cargo_empresa', models.CharField(max_length=30)),
                ('empresa', models.CharField(max_length=30)),
                ('actividad_empresa', models.CharField(max_length=30)),
                ('direccion_empresa', models.CharField(max_length=100)),
                ('telefono_empresa', models.CharField(max_length=30)),
                ('fax_empresa', models.CharField(max_length=30)),
                ('correo_trabajo', models.EmailField(max_length=254)),
                ('ilicito', models.BooleanField(default=False)),
                ('politico_expuesto', models.BooleanField(default=False)),
                ('cargo_politico', models.CharField(max_length=30)),
                ('periodo_politico', models.CharField(max_length=30)),
                ('nombre_politico', models.CharField(max_length=30, blank=True)),
                ('relacion_politico', models.CharField(max_length=30, blank=True)),
                ('declaracion_prima', models.BooleanField(default=False)),
                ('actividad_principal', models.CharField(max_length=100, blank=True)),
                ('ingreso_principal', models.CharField(default=b'<10,000.00', max_length=30, choices=[(b'<10,000.00', b'<10,000.00'), (b'10,000.00-30,000.00', b'10,000.00-30,000.00'), (b'30,000.00-50,000.00', b'30,000.00-50,000.00'), (b'>50,000.00', b'>50,000.00')])),
                ('otra_actividad', models.CharField(max_length=100, blank=True)),
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
