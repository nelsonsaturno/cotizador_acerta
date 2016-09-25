# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0007_auto_20160925_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='fax_empresa',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
