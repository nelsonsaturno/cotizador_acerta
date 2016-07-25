#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from cotizar.models import *


class ConductorVehiculoForm(forms.ModelForm):

    tipo_id = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.RadioSelect(), label="")
    valor_text = forms.CharField(label="Valor", help_text='Ex: 99,999.99')

    class Meta:
        model = ConductorVehiculo
        exclude = ['corredor', ]

        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'sexo': 'Sexo',
            'identificacion': 'Identificación',
            'estado_civil': 'Estado Civil',
            'correo': 'Correo',
            'telefono1': 'Teléfono Celular',
            'telefono2': 'Teléfono de Trabajo',
            'historial_transito': 'Historial de Tránsito',
            'edad': 'Edad',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'anio': 'Año',
            'cero_km': '0 Kms',
            'valor': 'Valor',
        }

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad < 18:
            raise forms.ValidationError(u'La edad minima debe ser 18 años.')
        return edad

    def clean_historial_transito(self):
        historial = self.cleaned_data.get('historial_transito')
        if historial > 10:
            raise forms.ValidationError(
                u'El máximo historial de tránsito es 10.')
        return historial

    def save(self, commit=True):
        conductor = super(ConductorVehiculoForm, self).save(commit=False)
        if commit:
            conductor.save()
            return conductor
        else:
            return conductor


class CotizacionUpdateForm(forms.Form):

    cuotas1 = forms.IntegerField(min_value=1, max_value=10, label="Cuotas", required=True)
    cuotas2 = forms.IntegerField(min_value=1, max_value=6, label="Cuotas", required=True)
    tipo_pago = forms.ChoiceField(choices=[(0, 'Pago de Contado'), (1, 'Pago Prima ACH/Visa'), (2, 'Otro')],
                                widget=forms.RadioSelect(), label="")    
    guardar = forms.CharField(widget=forms.HiddenInput(), required=False)
