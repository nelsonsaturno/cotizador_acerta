# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('darientSessions', '0034_auto_20160929_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='PolizasCorredor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('polizas_desde', models.PositiveIntegerField(default=1)),
                ('polizas_hasta', models.PositiveIntegerField(default=50000)),
                ('polizas', models.PositiveIntegerField(default=1)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
