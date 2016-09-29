# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0021_auto_20160929_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extradatoscliente',
            name='cargo_empresa',
        ),
        migrations.RemoveField(
            model_name='extradatoscliente',
            name='fax_empresa',
        ),
    ]
