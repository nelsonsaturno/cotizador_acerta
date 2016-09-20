# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('darientSessions', '0021_auto_20160920_0412'),
    ]

    operations = [
        migrations.AddField(
            model_name='datoscorredor',
            name='planes',
            field=models.CharField(default=b'-', max_length=100, choices=[(b'Plan 1', b'Plan 1'), (b'Plan 2', b'Plan 2'), (b'Plan 3', b'Plan 3')]),
        ),
    ]
