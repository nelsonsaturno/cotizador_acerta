# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('darientSessions', '0028_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datoscorredor',
            name='planes',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2016, 9, 25)),
        ),
    ]
