# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('darientSessions', '0036_auto_20160929_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polizascorredor',
            name='user',
            field=models.OneToOneField(related_name='polizas', to=settings.AUTH_USER_MODEL),
        ),
    ]
