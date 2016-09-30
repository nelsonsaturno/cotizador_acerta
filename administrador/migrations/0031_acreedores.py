# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0030_endosohistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acreedores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_acreedor', models.CharField(max_length=256)),
                ('tipo_id', models.CharField(max_length=20)),
                ('serie_id', models.IntegerField()),
                ('num_id', models.IntegerField()),
                ('dvid', models.CharField(max_length=2)),
            ],
        ),
    ]
