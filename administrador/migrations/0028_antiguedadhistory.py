# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrador', '0027_gastoshistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='AntiguedadHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('limite', models.IntegerField(default=1)),
                ('factor_mayor', models.FloatField(default=0.0)),
                ('factor_menor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.Antiguedad')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
