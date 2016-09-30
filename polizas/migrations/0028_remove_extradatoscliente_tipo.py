# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0027_auto_20160930_0048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extradatoscliente',
            name='tipo',
        ),
    ]
