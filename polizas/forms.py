#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from datetime import *
from bootstrap3_datetime.widgets import DateTimePicker
from polizas.models import *


class SolicitudClienteForm(forms.ModelForm):
    valido_desde = forms.DateField(
        label='Desde', required=True,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    valido_hasta = forms.DateField(
        label='Hasta', required=True,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    nombre_conductor = forms.CharField(label='Nombre')
    id_conductor = forms.CharField(label='Identificacion')
    nombre_responsable = forms.CharField(label='Nombre')
    id_responsable = forms.CharField(label='Identificacion')
    tipo_id_conductor = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.RadioSelect(), label="")
    tipo_id_responsable = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.RadioSelect(), label="")
    acreedor = forms.CharField(label='Acreedor Hipotecario')
    leasing = forms.CharField(label='o Leasing')
    agrupador = forms.CharField(label='')
    cobrador = forms.CharField(label='')
    dir_cobro = forms.CharField(label='')
    observaciones = forms.CharField(label='Observaciones')
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
            'dv': 'D.V',
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
            'recursos': 'Recursos',
        }

