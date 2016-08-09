# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0002_auto_20160806_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud',
            name='apartado',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='chasis',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='fax',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='motor',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='telefono_res',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='tipo',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='zona',
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='apartado',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='chasis',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='direccion',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='fax',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='motor',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='telefono_res',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='tipo',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='zona',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
