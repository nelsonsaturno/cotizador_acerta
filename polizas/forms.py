#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from datetime import *
from bootstrap3_datetime.widgets import DateTimePicker
from polizas.models import *


class SolicitudClienteForm(forms.ModelForm):
    valido_desde = forms.DateField(label='Vigencia Desde', required=True)
    valido_hasta = forms.DateField(label='Vigencia Hasta', required=True)
    nombre_conductor = forms.CharField(label='Nombre')
    id_conductor = forms.CharField(label='Identificacion')
    responsable = forms.ChoiceField(choices=[(0, 'Contratante'), (1, 'Asegurado'), (2, 'Otro')],
                                widget=forms.RadioSelect(), label="")
    nombre_responsable = forms.CharField(label='Nombre Completo')
    id_responsable = forms.CharField(label='Identificacion')
    tipo_id_conductor = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.RadioSelect(), label="")
    tipo_id_responsable = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.RadioSelect(), label="")
    acreedor = forms.CharField(label='Acreedor Hipotecario')
    leasing = forms.CharField(label='o Leasing')
    observaciones = forms.CharField(label='Observaciones')
    tipo_tdc = forms.ChoiceField(choices=[(0, 'Visa'), (1, 'Master Card'), (2, 'Dinners'), (3, 'American Express')],
                                widget=forms.RadioSelect(), label="", required=False)
    num_tdc = forms.CharField(label='Numero de Tarjeta',required=False)
    banco_tdc = forms.CharField(label='Banco',required=False)
    expiracion_tdc = forms.DateField(label='Fecha de Expiracion', required=False)
    dia_pago = forms.DateField(label='Dia de pago', required=True)
    nom_ref_personal = forms.CharField(label='Nombre o Razon Social')
    actividad_ref_personal = forms.CharField(label='Actividad')
    relacion_ref_personal = forms.CharField(label='Relacion con el cliente')
    telefono_ref_personal = forms.CharField(label='Telefono de contacto')
    nom_ref_bancaria = forms.CharField(label='Nombre o Razon Social')
    actividad_ref_bancaria = forms.CharField(label='Actividad')
    relacion_ref_bancaria = forms.CharField(label='Relacion con el cliente')
    telefono_ref_bancaria = forms.CharField(label='Telefono de contacto')
    nom_ref_comercial = forms.CharField(label='Nombre o Razon Social')
    actividad_ref_comercial = forms.CharField(label='Actividad')
    relacion_ref_comercial = forms.CharField(label='Relacion con el cliente')
    telefono_ref_comercial = forms.CharField(label='Telefono de contacto')
    firmador = forms.CharField(label='Nombre de quien firma')
    tipo_produccion = forms.ChoiceField(choices=[(0, 'Produccion Propia'), (1, 'Coaseguro Lider'), (2, 'Coaseguro No Lider'), (3, 'Reaseguro Cedido')],
                                widget=forms.Select(), label="")
    tipo_suscripcion = forms.ChoiceField(choices=[(0, 'Individual'), (1, 'Colectiva')],
                                widget=forms.Select(), label="")
    forma_facturacion = forms.ChoiceField(choices=[(0, 'Por Poliza'), (1, 'Por Certificado')],
                                widget=forms.Select(), label="")
    renovacion = forms.BooleanField(label='Renovacion Automatica')
    comision = forms.BooleanField(label='Comision estandar')
    def_comision = forms.CharField(label='Definir Comision')
    grupo_economico = forms.CharField(label='Grupo Economico')
    aprobaciones = forms.CharField(label='Aprobaciones especiales', widget=forms.Textarea())
    funcionario = forms.CharField(label='Nombre Completo')
    cargo_funcionario = forms.CharField(label='Cargo')
    area_funcionario = forms.ChoiceField(choices=[(0, 'Comercial'), (1, 'At. al Cliente'), (2, 'Fianzas'), (3, 'Seguros'), (4, 'Otras')],
                                widget=forms.Select(), label="")
    otra_area = forms.CharField(label='Otra area')

    class Meta:
        model = ExtraDatosCliente
        exclude = ['conductor', 'ref_personal', 'ref_bancaria', 'ref_comercial', ]

        labels = {
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
            'fax': 'Fax',
            'estafeta': 'Estafeta',
            'ocupacion': 'Ocupacion',
            'profesion': 'Profesion',
            'cargo_empresa': 'Cargo',
            'empresa': 'Lugar de Trabajo',
            'actividad_empresa': 'Actividad de Empresa',
            'direccion_empresa': 'Direccion Empresa',
            'telefono_empresa': 'Telefono de Trabajo',
            'fax_empresa': 'Fax de Trabajo',
            'correo_trabajo': 'Correo Electronico de Oficina',
            'politico_expuesto': 'Es o ha sido objeto de investigacion, indagacion o condena por actividades ilicitas, o delitos de lavado o blanqueo de dinero o financiamiento de terrorismo',
            'ilicito': 'Es o ha sido una (1) Persona Politicamente Expuesta, (2) familiar cercano, o (3) estrecho colaborador de esta',
            'cargo_politico': 'Cargo',
            'periodo_politico': 'Periodo',
            'nombre_politico': 'Nombre',
            'relacion_politico': 'Relacion',
            'declaracion_prima': 'Prima de Seguros mayor o igual a B./ 10,000.00',
            'actividad_principal': 'Actividad fuente principal de sus ingresos',
            'otra_actividad': 'Actividad de otras fuentes de ingreso:',
        }


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
