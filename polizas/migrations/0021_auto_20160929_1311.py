# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0020_auto_20160928_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='extradatoscliente',
            name='es_juridico',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='juridico_RUC',
            field=models.CharField(default=b'', max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='juridico_fecha_constitucion',
            field=models.CharField(default=b'', max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='juridico_pais_procedencia',
            field=models.CharField(default=b'', max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='juridico_razon_social',
            field=models.CharField(default=b'', max_length=30, blank=True),
        ),
    ]
