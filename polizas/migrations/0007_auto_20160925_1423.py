# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0006_auto_20160924_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='apartado_postal',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='apellido_cas',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='apto',
            field=models.CharField(default=b'', max_length=5, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='calle_ave',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='correo_trabajo',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='edificio',
            field=models.CharField(default=b'', max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='estafeta',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='fax',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='no_casa',
            field=models.CharField(default=b'', max_length=5, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='piso',
            field=models.CharField(default=b'', max_length=5, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='telefono_empresa',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='telefono_res',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
