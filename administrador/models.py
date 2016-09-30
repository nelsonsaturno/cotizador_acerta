#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

fs = FileSystemStorage(location='/cotizador_acerta/static/pdf')


class Sexo(models.Model):

    sexo = models.CharField(max_length=20, default='Masculino', blank=False,
                            choices=[('Masculino', 'Masculino'),
                                     ('Femenino', 'Femenino')], unique=True)
    factor = models.FloatField(blank=False, default=0.0)

    def __str__(self):
        return self.sexo


class SexoHistory(models.Model):

    prev_value = models.ForeignKey(Sexo)
    factor = models.FloatField(blank=False, default=0.0)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)


class Estado_Civil(models.Model):

    estado_civil = models.CharField(max_length=25, default='Soltero(a)',
                                    choices=[
                                        ('Soltero(a)', 'Soltero(a)'),
                                        ('Casado(a)', 'Casado(a)'),
                                        ('Otro', 'Otro')
                                    ], unique=True, blank=False)
    factor = models.FloatField(blank=False, default=0.0)


class EstadoCivilHistory(models.Model):

    prev_value = models.ForeignKey(Estado_Civil)
    factor = models.FloatField(blank=False, default=0.0)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)


class Valor(models.Model):

    inferior = models.FloatField(blank=False, default=0.0, unique=True)
    superior = models.FloatField(blank=False, default=0.0, unique=True)
    factor = models.FloatField(blank=False, default=0.0)


class ValorHistory(models.Model):

    prev_value = models.ForeignKey(Valor)
    inferior = models.FloatField(blank=False, default=0.0)
    superior = models.FloatField(blank=False, default=0.0)
    factor = models.FloatField(blank=False, default=0.0)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)


class Historial_Transito(models.Model):

    inferior = models.IntegerField(blank=False, default=0, unique=True,
                                   choices=[
                                       (0, 0),
                                       (4, 4),
                                       (8, 8)
                                   ])
    superior = models.IntegerField(blank=False, default=0, unique=True,
                                   choices=[
                                       (3, 3),
                                       (7, 7),
                                       (10, 10)
                                   ])
    factor = models.FloatField(blank=False, default=0.0)


class HistorialHistory(models.Model):

    prev_value = models.ForeignKey(Historial_Transito)
    inferior = models.IntegerField(blank=False, default=0,
                                   choices=[
                                       (0, 0),
                                       (4, 4),
                                       (8, 8)
                                   ])
    superior = models.IntegerField(blank=False, default=0,
                                   choices=[
                                       (3, 3),
                                       (7, 7),
                                       (10, 10)
                                   ])
    factor = models.FloatField(blank=False, default=0.0)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)


class Antiguedad(models.Model):

    limite = models.IntegerField(blank=False, default=1)
    factor_mayor = models.FloatField(blank=False, default=0.0)
    factor_menor = models.FloatField(blank=False, default=0.0)


class AntiguedadHistory(models.Model):

    prev_value = models.ForeignKey(Antiguedad)
    limite = models.IntegerField(blank=False, default=1)
    factor_mayor = models.FloatField(blank=False, default=0.0)
    factor_menor = models.FloatField(blank=False, default=0.0)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)


class Edad(models.Model):

    inferior = models.IntegerField(blank=False, default=0, unique=True,
                                   choices=[
                                       (18, 18),
                                       (26, 26),
                                       (66, 66)
                                   ])
    superior = models.IntegerField(blank=False, default=0, unique=True,
                                   choices=[
                                       (25, 25),
                                       (65, 65),
                                       (110, 110)
                                   ])
    factor = models.FloatField(blank=False, default=0.0)


class EdadHistory(models.Model):

    prev_value = models.ForeignKey(Edad)
    inferior = models.IntegerField(blank=False, default=0,
                                   choices=[
                                       (18, 18),
                                       (26, 26),
                                       (66, 66)
                                   ])
    superior = models.IntegerField(blank=False, default=0,
                                   choices=[
                                       (25, 25),
                                       (65, 65),
                                       (110, 110)
                                   ])
    factor = models.FloatField(blank=False, default=0.0)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)


class Tiempo_Uso(models.Model):

    tiempo = models.IntegerField(blank=False, default=0, unique=True,
                                 choices=[
                                     (1, 1),
                                     (2, 2),
                                     (3, 3),
                                     (4, 4),
                                     (5, 5),
                                     (6, 6),
                                     (7, 7),
                                     (8, 8),
                                     (9, 9),
                                 ])
    factor = models.FloatField(blank=False, default=0.0)


class TiempoUsoHistory(models.Model):

    prev_value = models.ForeignKey(Tiempo_Uso)
    factor = models.FloatField(blank=False, default=0.0)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)


class Colision(models.Model):

    tiempo = models.IntegerField(blank=False, default=0, unique=True,
                                 choices=[
                                     (1, 1),
                                     (2, 2),
                                     (3, 3),
                                     (4, 4),
                                     (5, 5),
                                     (6, 6),
                                     (7, 7),
                                     (8, 8),
                                     (9, 9),
                                 ])
    factor = models.FloatField(blank=False, default=0.0)


class ColisionHistory(models.Model):

    prev_value = models.ForeignKey(Colision)
    factor = models.FloatField(blank=False, default=0.0)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)


class Importacion(models.Model):

    factor = models.FloatField(blank=False, default=0.0)


class ImportacionHistory(models.Model):

    prev_value = models.ForeignKey(Importacion)
    factor = models.FloatField(blank=False, default=0.0)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)


class Endoso(models.Model):

    endoso = models.CharField(max_length=30, blank=False, unique=True,
                              default='Basico')
    precio = models.FloatField(blank=False, default=0.0)
    archivo = models.FileField(upload_to='cotizador_acerta/static/pdf')

    def __str__(self):
        return self.endoso


class EndosoHistory(models.Model):

    prev_value = models.ForeignKey(Endoso)
    endoso = models.CharField(max_length=30, blank=False, default='Basico')
    precio = models.FloatField(blank=False, default=0.0)
    archivo = models.CharField(max_length=200, blank=False, default='a.pdf')
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)


class LesionesCorporales(models.Model):

    lesiones_corporales = models.CharField(max_length=30, blank=False,
                                           unique=True,
                                           default='25,000.00/50,000.00',
                                           choices=[('5,000.00/10,000.00',
                                                     '5,000.00/10,000.00'),
                                                    ('10,000.00/20,000.00',
                                                     '10,000.00/20,000.00'),
                                                    ('20,000.00/40,000.00',
                                                     '20,000.00/40,000.00'),
                                                    ('25,000.00/50,000.00',
                                                     '25,000.00/50,000.00'),
                                                    ('50,000.00/100,000.00',
                                                     '50,000.00/100,000.00'),
                                                    ('100,000.00/300,000.00',
                                                     '100,000.00/300,000.00')])
    factor = models.FloatField(blank=False, default=0.0)


class LesionesCorporalesHistory(models.Model):

    prev_value = models.ForeignKey(LesionesCorporales)
    factor = models.FloatField(blank=False, default=0.0)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)


class DaniosPropiedad(models.Model):

    danios_propiedad = models.CharField(max_length=30, blank=False,
                                        unique=True,
                                        default='50,000.00',
                                        choices=[('10,000.00', '10,000.00'),
                                                 ('15,000.00', '15,000.00'),
                                                 ('20,000.00', '20,000.00'),
                                                 ('25,000.00', '25,000.00'),
                                                 ('50,000.00', '50,000.00'),
                                                 ('100,000.00', '100,000.00')])
    factor = models.FloatField(blank=False, default=0.0)


class DaniosHistory(models.Model):

    prev_value = models.ForeignKey(DaniosPropiedad)
    factor = models.FloatField(blank=False, default=0.0)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)


class GastosMedicos(models.Model):

    gastos_medicos = models.CharField(max_length=30, blank=False,
                                      unique=True,
                                      default='2,000.00/10,000.00',
                                      choices=[('500.00/2,500.00',
                                                '500.00/2,500.00'),
                                               ('1,000.00/5,000.00',
                                                '1,000.00/5,000.00'),
                                               ('2,000.00/10,000.00',
                                                '2,000.00/10,000.00'),
                                               ('5,000.00/25,000.00',
                                                '5,000.00/25,000.00'),
                                               ('5,000.00/35,000.00',
                                                '5,000.00/35,000.00'),
                                               ('10,000.00/50,000.00',
                                                '10,000.00/50,000.00')])
    factor = models.FloatField(blank=False, default=0.0)


class GastosHistory(models.Model):

    prev_value = models.ForeignKey(GastosMedicos)
    factor = models.FloatField(blank=False, default=0.0)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now_add=True)

class Acreedores(models.Model):

    nombre_acreedor = models.CharField(max_length=256, blank=False)
    tipo_id = models.CharField(max_length=20, blank=False)
    serie_id = models.IntegerField(blank=False)
    num_id = models.IntegerField(blank=False)
    dvid = models.CharField(max_length=2, blank=False)

class TipoVehiculo(models.Model):

      tipolval = models.CharField(max_length=30, blank=False)
      codlval = models.IntegerField(blank=False)
      descrip = models.CharField(max_length=256, blank=False)
