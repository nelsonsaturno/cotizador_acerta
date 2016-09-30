# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0031_acreedores'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoVehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipolval', models.CharField(max_length=30)),
                ('codlval', models.IntegerField()),
                ('descrip', models.CharField(max_length=256)),
            ],
        ),
    ]
