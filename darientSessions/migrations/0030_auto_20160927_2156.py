# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('darientSessions', '0029_auto_20160925_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='datoscorredor',
            name='planes',
            field=models.CharField(default=b'-', max_length=100, choices=[(b'Plan 1', b'Plan 1'), (b'Plan 2', b'Plan 2'), (b'Plan 3', b'Plan 3')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2016, 9, 27)),
        ),
    ]
