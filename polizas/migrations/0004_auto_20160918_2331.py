# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0003_auto_20160918_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extradatoscliente',
            name='documento',
            field=models.NullBooleanField(default=False),
        ),
    ]
