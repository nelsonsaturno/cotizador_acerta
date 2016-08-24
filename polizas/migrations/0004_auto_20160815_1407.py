# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0003_auto_20160809_0331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extradatoscliente',
            old_name='cargo',
            new_name='actividad_empresa',
        ),
        migrations.RenameField(
            model_name='extradatoscliente',
            old_name='fax_emp',
            new_name='apartado_postal',
        ),
        migrations.RenameField(
            model_name='extradatoscliente',
            old_name='profesion',
            new_name='calle_ave',
        ),
        migrations.RenameField(
            model_name='extradatoscliente',
            old_name='residencia',
            new_name='cargo_empresa',
        ),
        migrations.RenameField(
            model_name='extradatoscliente',
            old_name='telefono_emp',
            new_name='corregimiento',
        ),
        migrations.RenameField(
            model_name='extradatoscliente',
            old_name='direccion',
            new_name='direccion_empresa',
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='apto',
            field=models.CharField(default=b'N/A', max_length=5),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='cargo_politico',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='distrito',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='edificio',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='estafeta',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='fax_empresa',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='no_casa',
            field=models.CharField(default=b'N/A', max_length=5),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='nombre_politico',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='pais_residencia',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='periodo_politico',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='piso',
            field=models.CharField(default=b'N/A', max_length=5),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='provincia',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='relacion_politico',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='telefono_empresa',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='urbanizacion',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
