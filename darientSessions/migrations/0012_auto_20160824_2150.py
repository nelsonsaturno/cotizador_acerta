# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('darientSessions', '0011_auto_20160824_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datoscorredor',
            name='licencia',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='datoscorredor',
            name='razon_social',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datoscorredor',
            name='ruc',
            field=models.CharField(max_length=100),
        ),
    ]
