from django.db import models
from cotizar.models import *
from django.contrib.auth.models import User


class Solicitud(models.Model):

    cotizacion = models.ForeignKey(Cotizacion, null=True)
    # Extra fields.
    operador = models.ForeignKey(User,null=False)
    direccion = models.CharField(max_length=100, blank=False)
    telefono_res = models.CharField(max_length=20, blank=False)
    fax = models.CharField(max_length=20, blank=False)
    apartado = models.CharField(max_length=100, blank=False)
    zona = models.CharField(max_length=20, blank=False)
    vigencia_desde = models.DateField()
    vigencia_hasta = models.DateField()
    acreedor = models.CharField(max_length=40, blank=False)
    motor = models.CharField(max_length=40, blank=False)
    chasis = models.CharField(max_length=40, blank=False)
    tipo = models.CharField(max_length=40, blank=False)
    opcion = models.CharField(max_length=40, blank=False)
    agrupador = models.CharField(max_length=40, blank=False)
    cobrador = models.CharField(max_length=40, blank=False)
    direccion_cobro = models.CharField(max_length=100, blank=False)

    def __str__(self):
        pass

class Operador(models.Model):
    conductor = models.ForeignKey(ConductorVehiculo, blank=False)
    nombre = models.CharField(max_length=20, blank=False)
    apellido = models.CharField(max_length=20, blank=False)
    identificacion = models.CharField(max_length=20, blank=False)
    fecha_nacimiento = models.DateField(blank=False)

    def __str__(self):
        pass
    