from django.db import models
from cotizar.models import *


class Solicitud(models.Model):

    cotizacion = models.ForeignKey(Cotizacion, null=True)
    # Extra fields.
    direccion = models.CharField(max_length=100, blank=False)
    telefono_res = models.CharField(max_length=20, blank=False)
    fax = models.CharField(max_length=20, blank=False)
    apartado = models.CharField(max_length=100, blank=False)
    apartado = models.CharField(max_length=100, blank=False)
    zona = models.CharField(max_length=20, blank=False)
    vigencia_desde = models.DateField()
    vigencia_hasta = models.DateField()
    acreedor = models.CharField(max_length=40, blank=False)

    class Meta:
        verbose_name = "solicitud"
        verbose_name_plural = "solicitudes"

    def __str__(self):
        pass
