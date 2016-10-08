# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polizas', '0008_auto_20161006_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudpoliza',
            name='dia_pago',
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='color',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AddField(
            model_name='extradatoscliente',
            name='num_puestos',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='cuenta_banco_nombre',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='cuenta_banco_num',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='cuenta_tipo',
            field=models.CharField(default=b'', max_length=30, null=True, choices=[(b'Ahorro', b'Ahorro'), (b'Corriente', b'Corriente')]),
        ),
        migrations.AddField(
            model_name='solicitudpoliza',
            name='dia_cobro',
            field=models.CharField(default=b'Solicitada', max_length=30, choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5'), (b'6', b'6'), (b'7', b'7'), (b'8', b'8'), (b'9', b'9'), (b'10', b'10'), (b'11', b'11'), (b'12', b'12'), (b'13', b'13'), (b'14', b'14'), (b'15', b'15'), (b'16', b'16'), (b'17', b'17'), (b'18', b'18'), (b'19', b'19'), (b'20', b'20'), (b'21', b'21'), (b'22', b'22'), (b'23', b'23'), (b'24', b'24'), (b'25', b'25'), (b'26', b'26'), (b'27', b'27'), (b'28', b'28'), (b'29', b'29'), (b'30', b'30')]),
        ),
        migrations.AlterField(
            model_name='extradatoscliente',
            name='juridico_fecha_constitucion',
            field=models.DateField(default=datetime.date(2016, 10, 8)),
        ),
    ]
