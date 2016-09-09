# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cotizar', '0035_marcahistory_modelohistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conductorvehiculo',
            name='edad',
        ),
        migrations.AddField(
            model_name='conductorvehiculo',
            name='fecha_nacimiento',
            field=models.DateField(default=datetime.datetime(2016, 8, 29, 15, 41, 36, 358871, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
