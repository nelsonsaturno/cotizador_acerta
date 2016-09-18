# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('darientSessions', '0017_auto_20160918_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datoscorredor',
            name='planes',
        ),
    ]
