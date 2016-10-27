# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cotizar.models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConductorVehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=20)),
                ('sexo', models.CharField(max_length=10, choices=[(b'Masculino', b'Masculino'), (b'Femenino', b'Femenino')])),
                ('identificacion', models.CharField(max_length=20)),
                ('estado_civil', models.CharField(max_length=10, choices=[(b'Soltero(a)', b'Soltero(a)'), (b'Casado(a)', b'Casado(a)'), (b'Otro', b'Otro')])),
                ('correo', models.EmailField(max_length=254)),
                ('telefono1', models.CharField(max_length=20)),
                ('telefono2', models.CharField(default=b'', max_length=20, blank=True)),
                ('historial_transito', cotizar.models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(0)])),
                ('fecha_nacimiento', models.DateField()),
                ('anio', cotizar.models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(2017), django.core.validators.MinValueValidator(1900)])),
                ('cero_km', models.BooleanField(default=False)),
                ('valor', models.PositiveIntegerField()),
                ('importacion_piezas', models.BooleanField(default=False)),
                ('lesiones_corporales', models.CharField(default=b'25,000.00/50,000.00', max_length=30, choices=[(b'5,000.00/10,000.00', b'5,000.00/10,000.00'), (b'10,000.00/20,000.00', b'10,000.00/20,000.00'), (b'20,000.00/40,000.00', b'20,000.00/40,000.00'), (b'25,000.00/50,000.00', b'25,000.00/50,000.00'), (b'50,000.00/100,000.00', b'50,000.00/100,000.00'), (b'100,000.00/300,000.00', b'100,000.00/300,000.00')])),
                ('danios_propiedad', models.CharField(default=b'50,000.00', max_length=30, choices=[(b'10,000.00', b'10,000.00'), (b'15,000.00', b'15,000.00'), (b'20,000.00', b'20,000.00'), (b'25,000.00', b'25,000.00'), (b'50,000.00', b'50,000.00'), (b'100,000.00', b'100,000.00')])),
                ('gastos_medicos', models.CharField(default=b'2,000.00/10,000.00', max_length=30, choices=[(b'500.00/2,500.00', b'500.00/2,500.00'), (b'1,000.00/5,000.00', b'1,000.00/5,000.00'), (b'2,000.00/10,000.00', b'2,000.00/10,000.00'), (b'5,000.00/25,000.00', b'5,000.00/25,000.00'), (b'5,000.00/35,000.00', b'5,000.00/35,000.00'), (b'10,000.00/50,000.00', b'10,000.00/50,000.00')])),
                ('muerte_accidental', models.CharField(default=b'5,000.00/25,000.00', max_length=30, choices=[(b'5,000.00/25,000.00', b'5,000.00/25,000.00')])),
                ('tipo_id', models.CharField(max_length=30, choices=[(b'Cedula', b'Cedula'), (b'Pasaporte', b'Pasaporte')])),
                ('corredor', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('endoso', models.ForeignKey(to='administrador.Endoso')),
            ],
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lesiones_corporales', models.CharField(default=b'25,000.00/50,000.00', max_length=30, choices=[(b'5,000.00/10,000.00', b'5,000.00/10,000.00'), (b'10,000.00/20,000.00', b'10,000.00/20,000.00'), (b'20,000.00/40,000.00', b'20,000.00/40,000.00'), (b'25,000.00/50,000.00', b'25,000.00/50,000.00'), (b'50,000.00/100,000.00', b'50,000.00/100,000.00'), (b'100,000.00/300,000.00', b'100,000.00/300,000.00')])),
                ('danios_propiedad', models.CharField(default=b'50,000.00', max_length=30, choices=[(b'10,000.00', b'10,000.00'), (b'15,000.00', b'15,000.00'), (b'20,000.00', b'20,000.00'), (b'25,000.00', b'25,000.00'), (b'50,000.00', b'50,000.00'), (b'100,000.00', b'100,000.00')])),
                ('gastos_medicos', models.CharField(default=b'2,000.00/10,000.00', max_length=30, choices=[(b'500.00/2,500.00', b'500.00/2,500.00'), (b'1,000.00/5,000.00', b'1,000.00/5,000.00'), (b'2,000.00/10,000.00', b'2,000.00/10,000.00'), (b'5,000.00/25,000.00', b'5,000.00/25,000.00'), (b'10,000.00/50,000.00', b'10,000.00/50,000.00'), (b'5,000.00/35,000.00', b'5,000.00/35,000.00')])),
                ('otros_danios', models.FloatField(default=0.0)),
                ('colision_vuelco', models.FloatField(default=0.0)),
                ('incendio_rayo', models.FloatField(default=0.0)),
                ('robo_hurto', models.FloatField(default=0.0)),
                ('muerte_accidental', models.CharField(default=b'5,000.00/25,000.00', max_length=30, choices=[(b'5,000.00/25,000.00', b'5,000.00/25,000.00')])),
                ('asistencia_legal', models.BooleanField(default=True)),
                ('importacion_piezas', models.BooleanField(default=False)),
                ('preferencial_plus', models.BooleanField(default=True)),
                ('prima_lesiones', models.FloatField(default=0.0)),
                ('prima_daniosProp', models.FloatField(default=0.0)),
                ('prima_gastosMedicos', models.FloatField(default=0.0)),
                ('prima_otrosDanios', models.FloatField(default=0.0)),
                ('prima_colisionVuelco', models.FloatField(default=0.0)),
                ('prima_preferencialPlus', models.FloatField(default=75.0)),
                ('subtotal', models.FloatField(default=0.0)),
                ('prima_mensual', models.FloatField(default=0.0)),
                ('prima_pagoContado', models.FloatField(default=0.0)),
                ('prima_pagoVisa', models.FloatField(default=0.0)),
                ('is_active', models.BooleanField(default=False)),
                ('descuento', models.FloatField(default=0.0)),
                ('total', models.FloatField(default=0.0)),
                ('impuestos', models.FloatField(default=0.0)),
                ('prima_importacion', models.FloatField(default=0.0)),
                ('plan', models.CharField(default=b'B\xc3\xa1sico', max_length=100)),
                ('cuota', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(10)])),
                ('prima_endoso', models.FloatField(default=0.0)),
                ('status', models.CharField(default=b'Enviada', max_length=30, choices=[(b'Enviada', b'Enviada'), (b'Guardada', b'Guardada'), (b'Aprobada', b'Aprobada'), (b'Rechazada', b'Rechazada')])),
                ('tipo_pago', models.CharField(default=b'Contado', max_length=30, choices=[(b'Contado', b'Contado'), (b'ACH', b'ACH'), (b'Visa', b'Visa'), (b'Otro', b'Otro')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('version', models.PositiveSmallIntegerField(default=1)),
                ('conductor', models.ForeignKey(to='cotizar.ConductorVehiculo')),
                ('corredor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('endoso', models.ForeignKey(to='administrador.Endoso')),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MarcaHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='cotizar.Marca')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=35)),
                ('descuento', models.FloatField(default=1.0)),
                ('recargo', models.FloatField(default=1.0)),
                ('marca', models.ForeignKey(to='cotizar.Marca')),
            ],
        ),
        migrations.CreateModel(
            name='ModeloHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('marca', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=35)),
                ('descuento', models.FloatField(default=1.0)),
                ('recargo', models.FloatField(default=1.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='cotizar.Modelo')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='conductorvehiculo',
            name='marca',
            field=models.ForeignKey(to='cotizar.Marca'),
        ),
        migrations.AddField(
            model_name='conductorvehiculo',
            name='modelo',
            field=models.ForeignKey(to='cotizar.Modelo'),
        ),
    ]
