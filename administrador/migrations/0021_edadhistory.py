# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrador', '0020_estadocivilhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='EdadHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inferior', models.IntegerField(default=0, choices=[(18, 18), (26, 26), (66, 66)])),
                ('superior', models.IntegerField(default=0, choices=[(25, 25), (65, 65), (110, 110)])),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.Historial_Transito')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
