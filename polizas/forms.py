#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from datetime import *
from bootstrap3_datetime.widgets import DateTimePicker
from polizas.models import *


class SolicitudClienteForm(forms.Form):
    valido_desde = forms.DateField(
        label='Desde', required=True,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    valido_hasta = forms.DateField(
        label='Hasta', required=True,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    nac_operador = forms.CharField(label="Fecha de Nacimiento")
    nombre_operador = forms.CharField(label='')
    apellido_operador = forms.CharField(label='')
    id_operador = forms.CharField(label='')
    nac_responsable = forms.CharField(label="Fecha de Nacimiento")
    nombre_responsable = forms.CharField(label='')
    apellido_responsable = forms.CharField(label='')
    id_responsable = forms.CharField(label='')
    tipo_id_operador = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.RadioSelect(), label="")
    tipo_id_responsable = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.RadioSelect(), label="")
    leasing = forms.CharField(label='')
    agrupador = forms.CharField(label='')
    cobrador = forms.CharField(label='')
    dir_cobro = forms.CharField(label='')
    observaciones = forms.CharField(label='')

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
            'cargo_empresa': 'Cargo',
            'empresa': 'Lugar de Trabajo',
            'actividad_empresa': 'Actividad de Empresa',
            'direccion_empresa': 'Direccion Empresa',
            'telefono_empresa': 'Telefono de Trabajo',
            'fax_empresa': 'Fax de Trabajo',
            'correo_trabajo': 'Correo de Trabajo',
            'cargo_politico': 'Cargo',
            'periodo_politico': 'Periodo',
            'nombre_politico': 'Nombre',
            'relacion_politico': 'Relacion',
            'recursos': 'Recursos',
        }

