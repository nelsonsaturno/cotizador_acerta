# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0006_extradatoscliente_dv'),
    ]

    operations = [
        migrations.AddField(
            model_name='extradatoscliente',
            name='pais_nacimiento',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
