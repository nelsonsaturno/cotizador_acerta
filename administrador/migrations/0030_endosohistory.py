# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrador', '0029_importacionhistory_valorhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='EndosoHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('endoso', models.CharField(default=b'Basico', max_length=30)),
                ('precio', models.FloatField(default=0.0)),
                ('archivo', models.CharField(default=b'a.pdf', max_length=200)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.Endoso')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
