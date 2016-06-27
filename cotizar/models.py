#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Marca(models.Model):

    nombre = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.nombre


class Modelo(models.Model):

    nombre = models.CharField(max_length=20, blank=False)
    marca = models.ForeignKey(Marca)
    descuento = models.FloatField(blank=False, default=1.00)

    def __str__(self):
        return self.nombre


class ConductorVehiculo(models.Model):

    corredor = models.ForeignKey(User, null=True)
    nombre = models.CharField(max_length=20, blank=False)
    apellido = models.CharField(max_length=20, blank=False)
    sexo = models.CharField(max_length=10, blank=False, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')])
    identificacion = models.CharField(max_length=20, blank=False)
    estado_civil = models.CharField(max_length=10, blank=False, choices=[('Soltero(a)', 'Soltero(a)'), ('Casado(a)', 'Casado(a)'), ('Otro', 'Otro')])
    correo = models.EmailField(blank=False)
    telefono1 = models.CharField(max_length=20, blank=False)
    telefono2 = models.CharField(max_length=20, blank=False, default=" ")
    historial_transito = models.PositiveSmallIntegerField(blank=False)
    edad = models.PositiveSmallIntegerField(blank=False, default=18)
    marca = models.ForeignKey(Marca, blank=False)
    modelo = models.ForeignKey(Modelo, blank=False)
    anio = models.PositiveSmallIntegerField(blank=False)
    valor = models.PositiveIntegerField(blank=False)
    importacion_piezas = models.BooleanField(default=False)
    lesiones_corporales = models.CharField(max_length=30, blank=False, default='25,000.00/50,000.00',
                                           choices=[('5,000.00/10,000.00', '5,000.00/10,000.00'),
                                                    ('10,000.00/20,000.00','10,000.00/20,000.00'),
                                                    ('20,000.00/40,000.00', '20,000.00/40,000.00'),
                                                    ('25,000.00/50,000.00', '25,000.00/50,000.00'),
                                                    ('50,000.00/100,000.00', '50,000.00/100,000.00'),
                                                    ('100,000.00/300,000.00', '100,000.00/300,000.00')])
    danios_propiedad = models.CharField(max_length=30, blank=False, default='50,000.00',
                                        choices=[('10,000.00', '10,000.00'),
                                                 ('15,000.00', '15,000.00'),
                                                 ('20,000.00', '20,000.00'),
                                                 ('25,000.00', '25,000.00'),
                                                 ('50,000.00', '50,000.00'),
                                                 ('100,000.00', '100,000.00')])
    gastos_medicos = models.CharField(max_length=30, blank=False, default='2,000.00/10,000.00',
                                      choices=[('500.00/2,500.00', '500.00/2,500.00'),
                                               ('1,000.00/5,000.00', '1,000.00/5,000.00'),
                                               ('2,000.00/10,000.00', '2,000.00/10,000.00'),
                                               ('5,000.00/25,000.00', '5,000.00/25,000.00'),
                                               ('10,000.00/50,000.00', '10,000.00/50,000.00'),
                                               ('5,000.00/35,000.00', '5,000.00/35,000.00')])
    muerte_accidental = models.CharField(max_length=30, blank=False, default='5,000.00/25,000.00')


class Cotizacion(models.Model):

    conductor = models.ForeignKey(ConductorVehiculo, blank=False)
    corredor = models.ForeignKey(User)
    lesiones_corporales = models.CharField(max_length=30, blank=False, default='25,000.00/50,000.00',
                                           choices=[('5,000.00/10,000.00', '5,000.00/10,000.00'),
                                                    ('10,000.00/20,000.00','10,000.00/20,000.00'),
                                                    ('20,000.00/40,000.00', '20,000.00/40,000.00'),
                                                    ('25,000.00/50,000.00', '25,000.00/50,000.00'),
                                                    ('50,000.00/100,000.00', '50,000.00/100,000.00'),
                                                    ('100,000.00/300,000.00', '100,000.00/300,000.00')])
    danios_propiedad = models.CharField(max_length=30, blank=False, default='50,000.00',
                                        choices=[('10,000.00', '10,000.00'),
                                                 ('15,000.00', '15,000.00'),
                                                 ('20,000.00', '20,000.00'),
                                                 ('25,000.00', '25,000.00'),
                                                 ('50,000.00', '50,000.00'),
                                                 ('100,000.00', '100,000.00')])
    gastos_medicos = models.CharField(max_length=30, blank=False, default='2,000.00/10,000.00',
                                      choices=[('500.00/2,500.00', '500.00/2,500.00'),
                                               ('1,000.00/5,000.00', '1,000.00/5,000.00'),
                                               ('2,000.00/10,000.00', '2,000.00/10,000.00'),
                                               ('5,000.00/25,000.00', '5,000.00/25,000.00'),
                                               ('10,000.00/50,000.00', '10,000.00/50,000.00'),
                                               ('5,000.00/35,000.00', '5,000.00/35,000.00')])
    otros_danios = models.FloatField(blank=False, default=0.00)
    colision_vuelco = models.FloatField(blank=False, default=0.00)
    incendio_rayo = models.FloatField(blank=False, default=0.00)
    robo_hurto = models.FloatField(blank=False, default=0.00)
    muerte_accidental = models.CharField(max_length=30, blank=False, default='5,000.00/25,000.00')
    asistencia_legal = models.BooleanField(default=True)
    importacion_piezas = models.BooleanField(default=False)
    preferencial_plus = models.BooleanField(default=True)
    prima_lesiones = models.FloatField(blank=False, default=0.00)
    prima_daniosProp = models.FloatField(blank=False, default=0.00)
    prima_gastosMedicos = models.FloatField(blank=False, default=0.00)
    prima_otrosDanios = models.FloatField(blank=False, default=0.00)
    prima_colisionVuelco = models.FloatField(default=0.00)
    prima_preferencialPlus = models.FloatField(default=75.00)
    subtotal = models.FloatField(blank=False, default=0.00)
    prima_mensual = models.FloatField(blank=False, default=0.00)
    prima_pagoContado = models.FloatField(blank=False, default=0.00)
    prima_pagoVisa = models.FloatField(blank=False, default=0.00)
    is_active = models.BooleanField(default=False)
    descuento = models.FloatField(default=0.0, blank=False)
    total = models.FloatField(blank=False, default=0.00)
    impuestos = models.FloatField(blank=False, default=0.00)
    prima_importacion = models.FloatField(blank=False, default=0.00)
    plan = models.CharField(max_length=10, default="Básico")
