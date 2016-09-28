from django.db import models
from cotizar.models import *


# Modelo para la solicitud de la poliza.
class SolicitudPoliza(models.Model):

    cotizacion = models.ForeignKey(Cotizacion, null=True)
    # Extra fields.
    nombre_conductor = models.CharField(max_length=20, blank=False)
    id_conductor = models.CharField(max_length=20, blank=False)
    nombre_conductor2 = models.CharField(max_length=20, null=True)
    id_conductor2 = models.CharField(max_length=20, null=True)
    nombre_conductor3 = models.CharField(max_length=20, null=True)
    id_conductor3 = models.CharField(max_length=20, null=True)
    vigencia_desde = models.DateField()
    vigencia_hasta = models.DateField()
    acreedor_leasing = models.CharField(max_length=30, blank=False,
                                   default='Ninguno',
                                   choices=[('Acreedor',
                                             'Acreedor'),
                                            ('Leasing',
                                             'Leasing'),
                                            ('Ninguno',
                                             'Ninguno')])
    acreedor = models.CharField(max_length=40, blank=False)
    leasing = models.CharField(max_length=40, blank=False)
    firmador = models.CharField(max_length=40, blank=False)
    observaciones = models.CharField(max_length=100, blank=False, default='')
    responsable = models.CharField(max_length=30, blank=False,
                                   default='Contratante',
                                   choices=[('Contratante',
                                             'Contratante'),
                                            ('Asegurado',
                                             'Asegurado'),
                                            ('Otro',
                                             'Otro')])
    nombre_responsable = models.CharField(max_length=20, blank=False)
    id_responsable = models.CharField(max_length=20, blank=False)
    tipo_produccion = models.CharField(max_length=30, blank=False,
                                   default='Propia',
                                   choices=[('Propia',
                                             'Propia'),
                                            ('Coaseguro Lider',
                                             'Coaseguro Lider'),
                                            ('Coaseguro No Lider',
                                             'Coaseguro No Lider'),
                                            ('Reaseguro Cedido',
                                             'Reaseguro Cedido')])
    tipo_suscripcion = models.CharField(max_length=30, blank=False,
                                   default='Individual',
                                   choices=[('Individual',
                                             'Individual'),
                                            ('Colectiva',
                                             'Colectiva')])
    forma_facturacion = models.CharField(max_length=30, blank=False,
                                   default='Por Poliza',
                                   choices=[('Por Poliza',
                                             'Por Poliza'),
                                            ('Por Certificado',
                                             'Por Certificado')])
    renovacion_automatica = models.BooleanField(default=False)
    comision = models.BooleanField(default=False)
    def_comision = models.CharField(max_length=30, blank=False)
    grupo_economico = models.CharField(max_length=50, blank=False)
    aprobaciones = models.CharField(max_length=200, blank=False)
    funcionario = models.CharField(max_length=50, blank=False)
    cargo_funcionario = models.CharField(max_length=20, blank=False)
    area_funcionario = models.CharField(max_length=30, blank=False,
                                   default='Comercial',
                                   choices=[('Comercial',
                                             'Comercial'),
                                            ('At. al Cliente',
                                             'At. al Cliente'),
                                            ('Fianzas',
                                             'Fianzas'),
                                            ('Seguros',
                                             'Seguros'),
                                            ('Otro',
                                             'Otro')])
    otra_area = models.CharField(max_length=20, blank=False)
    tipo_tdc = models.CharField(max_length=30, blank=False, null=True,
                                   default='Visa',
                                   choices=[('Visa',
                                             'Visa'),
                                            ('Mastercard',
                                             'Mastercad')])
    num_tdc = models.CharField(max_length=20, blank=False, null=True)
    banco_tdc = models.CharField(max_length=20, blank=False, null=True)
    expiracion_tdc = models.CharField(max_length=20, blank=False, null=True)
    dia_pago = models.DateField()
    tipo = models.CharField(max_length=30, blank=False,
                                   default='Solicitada',
                                   choices=[('Solicitada',
                                             'Solicitada'),
                                            ('Emitida',
                                             'Emitida')])


class Referencia(models.Model):
    nombre = models.CharField(max_length=40, blank=False)
    actividad = models.CharField(max_length=40, blank=False)
    relacion = models.CharField(max_length=20, blank=False)
    telefono = models.CharField(max_length=20, blank=False)


# Datos extras para el formulario unico.
class ExtraDatosCliente(models.Model):
    conductor = models.ForeignKey(ConductorVehiculo, null=True, related_name='datos')
    placa = models.CharField(max_length=40, blank=False, null=True)
    motor = models.CharField(max_length=40, blank=False)
    chasis = models.CharField(max_length=40, blank=False)
    tipo = models.CharField(max_length=40, blank=False)
    nombre2 = models.CharField(max_length=20, blank=False)
    apellido_mat = models.CharField(max_length=20, blank=False)
    apellido_cas = models.CharField(max_length=20, blank=True)
    nacionalidad = models.CharField(max_length=30, blank=False)
    pais_nacimiento = models.CharField(max_length=30, blank=False)
    pais_residencia = models.CharField(max_length=30, blank=False)
    provincia = models.CharField(max_length=30, blank=False)
    distrito = models.CharField(max_length=30, blank=False)
    corregimiento = models.CharField(max_length=30, blank=False)
    urbanizacion = models.CharField(max_length=30, blank=False)
    edificio = models.CharField(max_length=30, blank=True, default='')
    piso = models.CharField(max_length=5, blank=True, default='')
    apto = models.CharField(max_length=5, blank=True, default='')
    calle_ave = models.CharField(max_length=30, blank=True)
    no_casa = models.CharField(max_length=5, blank=True, default='')
    apartado_postal = models.CharField(max_length=30, blank=True)
    telefono_res = models.CharField(max_length=20, blank=True)
    profesion = models.CharField(max_length=30, blank=False)
    ocupacion = models.CharField(max_length=30, blank=False)
    cargo_empresa = models.CharField(max_length=30, blank=False)
    empresa = models.CharField(max_length=30, blank=False)
    actividad_empresa = models.CharField(max_length=30, blank=False)
    direccion_empresa = models.CharField(max_length=100, blank=False)
    telefono_empresa = models.CharField(max_length=30, blank=True)
    fax_empresa = models.CharField(max_length=30, blank=True)
    correo_trabajo = models.EmailField(blank=True)
    ilicito = models.CharField(max_length=30,
                               blank=True,
                               default='',
                               choices=[('Si', 'Si'),
                               ('No', 'No')])
    politico_expuesto = models.CharField(max_length=30,
                                         blank=True,
                                         default='',
                                         choices=[('Si', 'Si'),
                                         ('No', 'No')])
    cargo_politico = models.CharField(max_length=30, blank=True)
    periodo_politico = models.CharField(max_length=30, blank=True)
    nombre_politico = models.CharField(max_length=30, blank=True)
    relacion_politico = models.CharField(max_length=30, blank=True)
    declaracion_prima = models.CharField(max_length=30,
                                         blank=True,
                                         default='',
                                         choices=[('Si', 'Si'),
                                         ('No', 'No')])
    # Perfil Financiero
    actividad_principal = models.CharField(max_length=100, blank=True)
    ingreso_principal = models.CharField(max_length=30, blank=True,
                                           default='<10,000.00',
                                           choices=[('<10,000.00',
                                                     '<10,000.00'),
                                                    ('10,000.00-30,000.00',
                                                     '10,000.00-30,000.00'),
                                                    ('30,000.00-50,000.00',
                                                     '30,000.00-50,000.00'),
                                                    ('>50,000.00',
                                                     '>50,000.00')])
    otra_actividad = models.CharField(max_length=100, blank=True)
    otro_ingreso = models.CharField(max_length=30, blank=True,
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
    ref_personal = models.ForeignKey(Referencia, null=True, related_name='personal')
    ref_bancaria = models.ForeignKey(Referencia, null=True, related_name='bancaria')
    ref_comercial = models.ForeignKey(Referencia, null=True, related_name='comercial')
    documento = models.NullBooleanField(default=False)
