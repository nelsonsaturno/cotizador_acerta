# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrador', '0017_sexohistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inferior', models.IntegerField(default=0, unique=True, choices=[(0, 0), (4, 4), (8, 8)])),
                ('superior', models.IntegerField(default=0, unique=True, choices=[(3, 3), (7, 7), (10, 10)])),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.Historial_Transito')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
