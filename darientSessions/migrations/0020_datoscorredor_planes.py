# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('darientSessions', '0019_auto_20160919_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='datoscorredor',
            name='planes',
            field=models.Field(default=b'', max_length=100, choices=[(b'Plan 1', b'Plan 1'), (b'Plan 2', b'Plan 2'), (b'Plan 3', b'Plan 3')]),
        ),
    ]
