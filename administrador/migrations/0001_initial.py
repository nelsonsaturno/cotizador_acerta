# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='Antiguedad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('limite', models.IntegerField(default=1)),
                ('factor_mayor', models.FloatField(default=0.0)),
                ('factor_menor', models.FloatField(default=0.0)),
            ],
        ),
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
        migrations.CreateModel(
            name='Colision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tiempo', models.IntegerField(default=0, unique=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])),
                ('factor', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='ColisionHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.Colision')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DaniosHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DaniosPropiedad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('danios_propiedad', models.CharField(default=b'50,000.00', unique=True, max_length=30, choices=[(b'10,000.00', b'10,000.00'), (b'15,000.00', b'15,000.00'), (b'20,000.00', b'20,000.00'), (b'25,000.00', b'25,000.00'), (b'50,000.00', b'50,000.00'), (b'100,000.00', b'100,000.00')])),
                ('factor', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Edad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inferior', models.IntegerField(default=0, unique=True, choices=[(18, 18), (26, 26), (66, 66)])),
                ('superior', models.IntegerField(default=0, unique=True, choices=[(25, 25), (65, 65), (110, 110)])),
                ('factor', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='EdadHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inferior', models.IntegerField(default=0, choices=[(18, 18), (26, 26), (66, 66)])),
                ('superior', models.IntegerField(default=0, choices=[(25, 25), (65, 65), (110, 110)])),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.Edad')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Endoso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('endoso', models.CharField(default=b'Basico', unique=True, max_length=30)),
                ('precio', models.FloatField(default=0.0)),
                ('archivo', models.FileField(upload_to=b'cotizador_acerta/static/pdf')),
            ],
        ),
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
        migrations.CreateModel(
            name='Estado_Civil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estado_civil', models.CharField(default=b'Soltero(a)', unique=True, max_length=25, choices=[(b'Soltero(a)', b'Soltero(a)'), (b'Casado(a)', b'Casado(a)'), (b'Otro', b'Otro')])),
                ('factor', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoCivilHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.Estado_Civil')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GastosHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GastosMedicos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gastos_medicos', models.CharField(default=b'2,000.00/10,000.00', unique=True, max_length=30, choices=[(b'500.00/2,500.00', b'500.00/2,500.00'), (b'1,000.00/5,000.00', b'1,000.00/5,000.00'), (b'2,000.00/10,000.00', b'2,000.00/10,000.00'), (b'5,000.00/25,000.00', b'5,000.00/25,000.00'), (b'5,000.00/35,000.00', b'5,000.00/35,000.00'), (b'10,000.00/50,000.00', b'10,000.00/50,000.00')])),
                ('factor', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Historial_Transito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inferior', models.IntegerField(default=0, unique=True, choices=[(0, 0), (4, 4), (8, 8)])),
                ('superior', models.IntegerField(default=0, unique=True, choices=[(3, 3), (7, 7), (10, 10)])),
                ('factor', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='HistorialHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inferior', models.IntegerField(default=0, choices=[(0, 0), (4, 4), (8, 8)])),
                ('superior', models.IntegerField(default=0, choices=[(3, 3), (7, 7), (10, 10)])),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.Historial_Transito')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Importacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factor', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='ImportacionHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.Importacion')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LesionesCorporales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lesiones_corporales', models.CharField(default=b'25,000.00/50,000.00', unique=True, max_length=30, choices=[(b'5,000.00/10,000.00', b'5,000.00/10,000.00'), (b'10,000.00/20,000.00', b'10,000.00/20,000.00'), (b'20,000.00/40,000.00', b'20,000.00/40,000.00'), (b'25,000.00/50,000.00', b'25,000.00/50,000.00'), (b'50,000.00/100,000.00', b'50,000.00/100,000.00'), (b'100,000.00/300,000.00', b'100,000.00/300,000.00')])),
                ('factor', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='LesionesCorporalesHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.LesionesCorporales')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sexo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sexo', models.CharField(default=b'Masculino', unique=True, max_length=20, choices=[(b'Masculino', b'Masculino'), (b'Femenino', b'Femenino')])),
                ('factor', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='SexoHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.Sexo')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tiempo_Uso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tiempo', models.IntegerField(default=0, unique=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])),
                ('factor', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='TiempoUsoHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.Tiempo_Uso')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TipoVehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipolval', models.CharField(max_length=30)),
                ('codlval', models.IntegerField()),
                ('descrip', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Valor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inferior', models.FloatField(default=0.0, unique=True)),
                ('superior', models.FloatField(default=0.0, unique=True)),
                ('factor', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='ValorHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inferior', models.FloatField(default=0.0)),
                ('superior', models.FloatField(default=0.0)),
                ('factor', models.FloatField(default=0.0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('prev_value', models.ForeignKey(to='administrador.Valor')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gastoshistory',
            name='prev_value',
            field=models.ForeignKey(to='administrador.GastosMedicos'),
        ),
        migrations.AddField(
            model_name='gastoshistory',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='danioshistory',
            name='prev_value',
            field=models.ForeignKey(to='administrador.DaniosPropiedad'),
        ),
        migrations.AddField(
            model_name='danioshistory',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
