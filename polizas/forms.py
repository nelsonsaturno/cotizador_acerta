#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from datetime import *
from bootstrap3_datetime.widgets import DateTimePicker
from polizas.models import *
from datetime import datetime as dt
import datetime
from django.conf import settings

def default_desde():
    if len(str(dt.now().month)) == 1:
        return str(dt.now().year) + '0' + str(dt.now().month) + str(dt.now().day)
    else:
        return str(dt.now().year) +  str(dt.now().month) + str(dt.now().day)

def default_hasta():
    if len(str(dt.now().month)) == 1:
        return str(dt.now().year + 1) + '0' + str(dt.now().month) + str(dt.now().day)
    else:
        return str(dt.now().year + 1) +  str(dt.now().month) + str(dt.now().day)

def get_acreedores_choices():
    choices = Acreedores.objects.all()
    acreedor_leasing = []
    for i in choices:
        acreedor_leasing.append((i.nombre_acreedor,i.nombre_acreedor))
    return acreedor_leasing

def get_tipo_choices():
    choices = TipoVehiculo.objects.all()
    tipos = []
    for i in choices:
        tipos.append((i.descrip, i.descrip))
    return tipos

class SolicitudClienteForm(forms.ModelForm):
    aseguradoConductor = forms.BooleanField(label='Asegurado es Conductor', required=False)
    asegurado = forms.CharField(label='Nombre', required=False)
    id_asegurado = forms.CharField(label='Identificacion', required=False)
    valido_desde = forms.DateField(label='Vigencia Desde', required=True, initial=date.today(), input_formats=settings.DATE_INPUT_FORMATS)
    valido_hasta = forms.DateField(label='Vigencia Hasta', required=False, input_formats=settings.DATE_INPUT_FORMATS)

    nombre_conductor = forms.CharField(label='Nombre', required=False)
    id_conductor = forms.CharField(label='Identificacion', required=False)
    nombre_conductor2 = forms.CharField(label='Nombre', required=False)
    id_conductor2 = forms.CharField(label='Identificacion', required=False)
    nombre_conductor3 = forms.CharField(label='Nombre', required=False)
    id_conductor3 = forms.CharField(label='Identificacion', required=False)

    provincia_1 = forms.ChoiceField(
        choices=[
            ('',''),
            (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),
            (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'),
            (11, '11'), (12, '12'), (13, '13'), ('PE', 'PE'),
            ('N', 'N'), ('E', 'E')
        ],
        required=False
    )

    tipo_1 = forms.ChoiceField(
        choices=[('',''), ('PI', 'PI'), ('AV', 'AV')],
        required=False
    )

    campo_id_1_1 = forms.CharField(
        label="Campo 1", required=False,
        localize=True, max_length=6
    )

    campo_id_2_1 = forms.CharField(
        label="Campo 2", required=False,
        localize=True, max_length=4
    )

    provincia_2 = forms.ChoiceField(
        choices=[
            ('',''),
            (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),
            (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'),
            (11, '11'), (12, '12'), (13, '13'), ('PE', 'PE'),
            ('N', 'N'), ('E', 'E')
        ],
        required=False
    )

    tipo_2 = forms.ChoiceField(
        choices=[('',''), ('PI', 'PI'), ('AV', 'AV')],
        required=False
    )

    campo_id_1_2 = forms.CharField(
        label="Campo 1", required=False,
        localize=True, max_length=6
    )

    campo_id_2_2 = forms.CharField(
        label="Campo 2", required=False,
        localize=True, max_length=4
    )

    provincia_3 = forms.ChoiceField(
        choices=[
            ('',''),
            (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),
            (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'),
            (11, '11'), (12, '12'), (13, '13'), ('PE', 'PE'),
            ('N', 'N'), ('E', 'E')
        ],
        required=False
    )

    tipo_3 = forms.ChoiceField(
        choices=[('',''), ('PI', 'PI'), ('AV', 'AV')],
        required=False
    )

    campo_id_1_3 = forms.CharField(
        label="Campo 1", required=False,
        localize=True, max_length=6
    )

    campo_id_2_3 = forms.CharField(
        label="Campo 2", required=False,
        localize=True, max_length=4
    )




    responsable = forms.ChoiceField(choices=[(0, 'Contratante'), (1, 'Asegurado'), (2, 'Otro')],
                                widget=forms.RadioSelect(), label="")
    nombre_responsable = forms.CharField(label='Nombre Completo', required=False)
    id_responsable = forms.CharField(label='Identificacion', required=False)
    tipo_id_conductor = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.Select(), label="", required=False)
    tipo_id_conductor2 = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.Select(), label="", required=False)
    tipo_id_conductor3 = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.Select(), label="", required=False)
    tipo_id_responsable = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.Select(), label="", required=False)
    acreedor_leasing = forms.ChoiceField(choices=get_acreedores_choices())

    tipo_acreedor_leasing = forms.ChoiceField(choices=[(1,'Acreedor'),(2,'Leasing')], required=False)
    observaciones = forms.CharField(label='Observaciones', widget=forms.Textarea(), required=False)
    tipo_tdc = forms.ChoiceField(choices=[(0, 'Visa'), (1, 'Master Card')],
                                widget=forms.RadioSelect(), label="", required=False)
    num_tdc = forms.CharField(label='Numero de Tarjeta',required=False)
    banco_tdc = forms.CharField(label='Banco',required=False)
    expiracion_tdc = forms.CharField(label='Expiracion',required=False)
    dia_pago = forms.DateField(label='Dia de pago (aaaa/mm/dd)', required=True, initial=default_desde)
    nom_ref_personal = forms.CharField(label='Nombre o Razon Social', required=False)
    actividad_ref_personal = forms.CharField(label='Actividad', required=False)
    relacion_ref_personal = forms.CharField(label='Relacion con el cliente', required=False)
    telefono_ref_personal = forms.CharField(label='Telefono de contacto', required=False)
    nom_ref_bancaria = forms.CharField(label='Nombre o Razon Social', required=False)
    actividad_ref_bancaria = forms.CharField(label='Actividad', required=False)
    relacion_ref_bancaria = forms.CharField(label='Relacion con el cliente', required=False)
    telefono_ref_bancaria = forms.CharField(label='Telefono de contacto', required=False)
    nom_ref_comercial = forms.CharField(label='Nombre o Razon Social', required=False)
    actividad_ref_comercial = forms.CharField(label='Actividad', required=False)
    relacion_ref_comercial = forms.CharField(label='Relacion con el cliente', required=False)
    telefono_ref_comercial = forms.CharField(label='Telefono de contacto', required=False)
    firmador = forms.CharField(label='Nombre de quien firma', required=False)
    tipo_produccion = forms.ChoiceField(choices=[(0, 'Produccion Propia'), (1, 'Coaseguro Lider'), (2, 'Coaseguro No Lider'), (3, 'Reaseguro Cedido')],
                                widget=forms.Select(), label="", required=False)
    tipo_suscripcion = forms.ChoiceField(choices=[(0, 'Individual'), (1, 'Colectiva')],
                                widget=forms.Select(), label="", required=False)
    forma_facturacion = forms.ChoiceField(choices=[(0, 'Por Poliza'), (1, 'Por Certificado')],
                                widget=forms.Select(), label="", required=False)
    renovacion = forms.BooleanField(label='Renovacion Automatica', required=False)
    comision = forms.BooleanField(label='Comision estandar', required=False)
    def_comision = forms.CharField(label='Definir Comision', required=False)
    grupo_economico = forms.CharField(label='Grupo Economico', required=False)
    aprobaciones = forms.CharField(label='Aprobaciones especiales', widget=forms.Textarea(), required=False)
    funcionario = forms.CharField(label='Nombre Completo', required=False)
    cargo_funcionario = forms.CharField(label='Cargo', required=False)
    area_funcionario = forms.ChoiceField(choices=[(0, 'Comercial'), (1, 'At. al Cliente'), (2, 'Fianzas'), (3, 'Seguros'), (4, 'Otras')],
                                widget=forms.Select(), label="", required=False)
    otra_area = forms.CharField(label='Otra area', required=False)

    placa = forms.CharField(label='Placa No.', required=False)
    tipo_vehiculo = forms.ChoiceField(choices=get_tipo_choices(), required=False)

    nombre2 = forms.CharField(label='Segundo Nombre', required=False)

    profesion = forms.CharField(label='Profesión', required=False)
    ocupacion = forms.CharField(label='Ocupación', required=False)
    empresa = forms.CharField(label='Lugar de Trabajo', required=False)
    actividad_empresa = forms.CharField(label='Actividad de Empresa', required=False)
    direccion_empresa = forms.CharField(label='Dirección Empresa', required=False)

    juridico_fecha_constitucion = forms.DateField(
        label='Fecha de constitución',
        input_formats=settings.DATE_INPUT_FORMATS, required=False)

    tipo_tdc = forms.ChoiceField(label="Tipo tarjeta de crédito",
                                 required=False,
                                 choices=[('Visa', 'Visa'),
                                    ('Mastercard', 'Mastercad')])
    banco_tdc = forms.CharField(label='Banco', required=False)

    class Meta:
        model = ExtraDatosCliente
        exclude = ['conductor', 'ref_personal', 'ref_bancaria', 'ref_comercial', ]

        labels = {
            'es_juridico': 'Contratante es persona juridica',
            'juridico_RUC': 'RUC',
            'juridico_razon_social': 'Razón Social',
            'juridico_pais_procedencia': 'País de procedencia',
            'juridico_fecha_constitucion': 'Fecha de constitución',
            'placa': 'Placa No.',
            'motor': 'Motor',
            'chasis': 'Chasis',
            'tipo': 'Tipo',
            'nombre2': 'Segundo Nombre',
            'apellido_mat': 'Apellido Materno',
            'apellido_cas': 'Apellido de Casado/a',
            'nacionalidad': 'Nacionalidad',
            'pais_nacimiento': 'Pais de Nacimiento',
            'pais_residencia': 'Pais de Residencia',
            'provincia': 'Provincia',
            'distrito': 'Distrito',
            'corregimiento': 'Corregimiento',
            'urbanizacion': 'Urbanizacion',
            'edificio': 'Edificio',
            'piso': 'Piso',
            'apto': 'Apto',
            'calle_ave': 'Calle o Ave',
            'no_casa': 'No. Casa',
            'apartado_postal': 'Apartado Postal',
            'telefono_res': 'Telefono Residencial',
            'ocupacion': 'Ocupacion',
            'profesion': 'Profesion',
            'empresa': 'Lugar de Trabajo',
            'actividad_empresa': 'Actividad de Empresa',
            'direccion_empresa': 'Direccion Empresa',
            'telefono_empresa': 'Telefono de Trabajo',
            'correo_trabajo': 'Correo Electronico de Oficina',
            'ilicito': 'Es o ha sido objeto de investigacion, indagacion o condena por actividades ilicitas, o delitos de lavado o blanqueo de dinero o financiamiento de terrorismo',
            'politico_expuesto': 'Es o ha sido una (1) Persona Politicamente Expuesta, (2) familiar cercano, o (3) estrecho colaborador de esta',
            'periodo_politico': 'Periodo',
            'nombre_politico': 'Nombre',
            'relacion_politico': 'Relacion',
            'declaracion_prima': 'Prima de Seguros mayor o igual a B./ 10,000.00',
            'actividad_principal': 'Actividad fuente principal de sus ingresos',
            'otra_actividad': 'Actividad de otras fuentes de ingreso:',
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudClienteForm, self).__init__(*args, **kwargs)
        self.fields['edificio'].initial = ''
        self.fields['piso'].initial = ''
        self.fields['apto'].initial = ''
        self.fields['no_casa'].initial = ''



class PagoForm(forms.Form):

    numero_tarjeta = forms.IntegerField(
        label="Número de Tarjeta",
        required=True,
        min_value=1
    )
    cvv = forms.IntegerField(
        label='CVV',
        required=True,
        widget=forms.PasswordInput(),
        min_value=0
    )
    # expiracion_tdc = forms.DateField(
    #     label='Fecha de Expiracion',
    #     required=True,
    #     widget=DateTimePicker(
    #         options={
    #             "format": "YYYY-MM-DD",
    #             "pickTime": False
    #         }
    #     )
    # )
    nombre_persona = forms.CharField(
        label='Nombre Impreso en la Tarjeta',
        required=True
    )
