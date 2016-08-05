#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from datetime import *
from bootstrap3_datetime.widgets import DateTimePicker
from polizas.models import *


class SolicitudPolizaForm(forms.Form):
    valido_desde = forms.DateField(
        label='Desde', required=True,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    valido_hasta = forms.DateField(
        label='Hasta', required=True,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    nac_operador = forms.CharField(label="Fecha de Nacimiento")
    nombre_operador = forms.Charfield(label='')
    apellido_operador = forms.Charfield(label='')
    id_operador = forms.Charfield(label='')
    tipo_id = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.RadioSelect(), label="")

    class Meta:
        model = Solicitud
        exclude = ['cotizacion', 'vigencia_desde', 'vigencia_hasta', 'operador', ]

        labels = {
            'direccion': 'Direccion',
            'telefono_res': 'Telefono Residencial',
            'fax': 'Fax',
            'apartado': 'Apartado',
            'zona': 'Zona',
            'acreedor': 'Acreedor',
            'motor': 'Motor',
            'chasis': 'Chasis',
            'tipo': 'Tipo',
            'opcion': 'Opcion',
            'agrupador': 'Agrupador',
            'cobrador': 'Cobrador',
            'direccion_cobro': 'Direccion de cobro',
        }
