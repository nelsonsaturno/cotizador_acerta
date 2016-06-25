#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models


class Sexo(models.Model):

    sexo = models.CharField(max_length=20, default='Masculino', blank=False,
                            choices=[('Masculino', 'Masculino'),
                                     ('Femenino', 'Femenino')], unique=True)
    factor = models.FloatField(blank=False, default=0.0)


class Estado_Civil(models.Model):

    estado_civil = models.CharField(max_length=25, default='Soltero(a)',
                                    choices=[
                                        ('Soltero(a)', 'Soltero(a)'),
                                        ('Casado(a)', 'Casado(a)'),
                                        ('Otro', 'Otro')
                                    ], unique=True, blank=False)
    factor = models.FloatField(blank=False, default=0.0)


class Valor(models.Model):

    inferior = models.FloatField(blank=False, default=0.0)
    superior = models.FloatField(blank=False, default=0.0)
    factor = models.FloatField(blank=False, default=0.0)


class Historial_Transito(models.Model):

    inferior = models.IntegerField(blank=False, default=0, unique=True,
                                   choices=[
                                       (1, 1),
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


class Antiguedad(models.Model):

    limite = models.IntegerField(blank=False, default=1)
    factor_mayor = models.FloatField(blank=False, default=0.0)
    factor_menor = models.FloatField(blank=False, default=0.0)


class Edad(models.Model):

    inferior = models.IntegerField(blank=False, default=0, unique=True,
                                   choices=[
                                       (1, 1),
                                       (26, 26)
                                   ])
    superior = models.IntegerField(blank=False, default=0, unique=True,
                                   choices=[
                                       (25, 25),
                                       (65, 65)
                                   ])
    factor = models.FloatField(blank=False, default=0.0)


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


class Importacion(models.Model):

    factor = models.FloatField(blank=False, default=0.0)


class Acerta_Preferencial(models.Model):

    factor = models.FloatField(blank=False, default=0.0)
