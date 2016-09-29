# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('darientSessions', '0035_polizascorredor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polizascorredor',
            name='polizas',
            field=models.IntegerField(default=0),
        ),
    ]
