from django.db import models
from cotizar.models import *


# Operador del automovil de la poliza.
class Operador(models.Model):
    nombre = models.CharField(max_length=20, blank=False)
    apellido = models.CharField(max_length=20, blank=False)
    identificacion = models.CharField(max_length=20, blank=False)
    fecha_nacimiento = models.DateField(blank=False)

    def __str__(self):
        return self.nombre + " " + self.apellido


# Modelo para la solicitud de la poliza.
class Solicitud(models.Model):

    cotizacion = models.ForeignKey(Cotizacion, null=True)
    # Extra fields.
    operador = models.ForeignKey(Operador, null=False)
    vigencia_desde = models.DateField()
    vigencia_hasta = models.DateField()
    acreedor = models.CharField(max_length=40, blank=False)
    opcion = models.CharField(max_length=40, blank=False)
    agrupador = models.CharField(max_length=40, blank=False)
    cobrador = models.CharField(max_length=40, blank=False)
    direccion_cobro = models.CharField(max_length=100, blank=False)

    def __str__(self):
        pass


class Referencia(models.Model):
    nombre = models.CharField(max_length=40, blank=False)
    actividad = models.CharField(max_length=40, blank=False)
    relacion = models.CharField(max_length=20, blank=False)
    telefono = models.CharField(max_length=20, blank=False)


# Datos extras para el formulario unico.
class ExtraDatosCliente(models.Model):
    conductor = models.ForeignKey(ConductorVehiculo, blank=False)
    telefono_res = models.CharField(max_length=20, blank=False)
    fax = models.CharField(max_length=20, blank=False)
    apartado = models.CharField(max_length=100, blank=False)
    zona = models.CharField(max_length=20, blank=False)
    motor = models.CharField(max_length=40, blank=False)
    chasis = models.CharField(max_length=40, blank=False)
    tipo = models.CharField(max_length=40, blank=False)
    nombre2 = models.CharField(max_length=20, blank=False)
    apellido_mat = models.CharField(max_length=20, blank=False)
    apellido_cas = models.CharField(max_length=20, blank=False)
    nacionalidad = models.CharField(max_length=30, blank=False)
    pais_residencia = models.CharField(max_length=30, blank=False)
    provincia = models.CharField(max_length=30, blank=False)
    distrito = models.CharField(max_length=30, blank=False)
    corregimiento = models.CharField(max_length=30, blank=False)
    urbanizacion = models.CharField(max_length=30, blank=False)
    edificio = models.CharField(max_length=30, blank=False, default='N/A')
    piso = models.CharField(max_length=5, blank=False, default='N/A')
    apto = models.CharField(max_length=5, blank=False, default='N/A')
    calle_ave = models.CharField(max_length=30, blank=False)
    no_casa = models.CharField(max_length=5, blank=False, default='N/A')
    apartado_postal = models.CharField(max_length=30, blank=False)
    estafeta = models.CharField(max_length=30, blank=False)
    ocupacion = models.CharField(max_length=30, blank=False)
    cargo_empresa = models.CharField(max_length=30, blank=False)
    empresa = models.CharField(max_length=30, blank=False)
    actividad_empresa = models.CharField(max_length=30, blank=False)
    direccion_empresa = models.CharField(max_length=100, blank=False)
    telefono_empresa = models.CharField(max_length=30, blank=False)
    fax_empresa = models.CharField(max_length=30, blank=False)
    correo_trabajo = models.EmailField(blank=False)
    politico_expuesto = models.BooleanField(default=False)
    cargo_politico = models.CharField(max_length=30, blank=False, default='N/A')
    periodo_politico = models.CharField(max_length=30, blank=False, default='N/A')
    nombre_politico = models.CharField(max_length=30, blank=False, default='N/A')
    relacion_politico = models.CharField(max_length=30, blank=False, default='N/A')
    declaracion_prima = models.BooleanField(default=False)
    recursos = models.CharField(max_length=100, blank=True)
    # Perfil Financiero
    ingreso_principal = models.CharField(max_length=30, blank=False,
                                           default='<10,000.00',
                                           choices=[('<10,000.00',
                                                     '<10,000.00'),
                                                    ('10,000.00-30,000.00',
                                                     '10,000.00-30,000.00'),
                                                    ('30,000.00-50,000.00',
                                                     '30,000.00-50,000.00'),
                                                    ('>50,000.00',
                                                     '>50,000.00')])
    otro_ingreso = models.CharField(max_length=30, blank=False,
                                           default='<10,000.00',
                                           choices=[('<10,000.00',
                                                     '<10,000.00'),
                                                    ('10,000.00-30,000.00',
                                                     '10,000.00-30,000.00'),
                                                    ('30,000.00-50,000.00',
                                                     '30,000.00-50,000.00'),
                                                    ('>50,000.00',
                                                     '>50,000.00')])
    # Referencias
    ref_personal = models.ForeignKey(Referencia, blank=False, related_name='personal')
    ref_bancaria = models.ForeignKey(Referencia, blank=False, related_name='bancaria')
    ref_comercial = models.ForeignKey(Referencia, blank=False, related_name='comercial')
    documento = models.BooleanField(default=False)


