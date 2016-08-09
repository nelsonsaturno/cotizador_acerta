# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0021_edadhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edadhistory',
            name='prev_value',
            field=models.ForeignKey(to='administrador.Edad'),
        ),
    ]
