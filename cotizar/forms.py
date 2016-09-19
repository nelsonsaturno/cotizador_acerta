#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from cotizar.models import *
from datetime import *
from bootstrap3_datetime.widgets import DateTimePicker
from django.contrib.auth.models import User
from darientSessions.models import CorredorVendedor
import datetime


class ConductorVehiculoForm(forms.ModelForm):

    tipo_id = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.RadioSelect(), label="")
    valor_text = forms.CharField(label="Valor", help_text='Ex: 99,999.99')

    mail_corredor = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = ConductorVehiculo
        exclude = ['corredor', ]

        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'identificacion': 'Identificación',
            'estado_civil': 'Estado Civil',
            'correo': 'Correo',
            'telefono1': 'Teléfono Celular',
            'telefono2': 'Teléfono de Trabajo',
            'historial_transito': 'Historial de Tránsito',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'anio': 'Año',
            'cero_km': '0 Kms',
            'valor': 'Valor',
        }
        widgets = {
            'marca': forms.Select(attrs={'class': 'select2'}),
            'modelo': forms.Select(attrs={'class': 'select2'}),
            'historial_transito': forms.Select(
                choices=[
                    (0, "0"), (1, "1"), (2, "2"), (3, "3"),
                    (4, "4"), (5, "5"), (6, "6"), (7, "7"),
                    (8, "8"), (9, "9"), (10, "10")
                ]
            )
        }

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        d = str(fecha)
        d1 = datetime.datetime.strptime(d, "%Y-%m-%d")
        d2 = datetime.datetime.now()
        d3 = (d2 - d1).days / 365
        if d3 < 18.0:
            raise forms.ValidationError(u'La edad minima debe ser 18 años.')
        return fecha

    def clean_historial_transito(self):
        historial = self.cleaned_data.get('historial_transito')
        if historial > 10:
            raise forms.ValidationError(
                u'El máximo historial de tránsito es 10.')
        return historial

    def clean(self):
        valor = self.cleaned_data['valor']
        if valor <= 75000.00:
            return self.cleaned_data
        else:
            if self.cleaned_data['mail_corredor'] == 'lhernandez@acertaseguros.com':
                return self.cleaned_data
            corredor = User.objects.get(email='lhernandez@acertaseguros.com')
            vendedores = CorredorVendedor.objects.filter(corredor=corredor)
            for vendedor in vendedores:
                if self.cleaned_data['mail_corredor'] == vendedor.vendedor.email:
                    return self.cleaned_data
            raise forms.ValidationError(u'Para cotizar vehículos con un valor superior a B/. 75,000.00 por favor contacte a su ejecutivo de Acerta Seguros.')

    def save(self, commit=True):
        conductor = super(ConductorVehiculoForm, self).save(commit=False)
        if commit:
            conductor.save()
            return conductor
        else:
            return conductor


class CotizacionUpdateForm(forms.Form):

    cuotas = forms.IntegerField(min_value=1, max_value=10, label="Cuotas", required=False, initial=1)
    cuotas2 = forms.IntegerField(min_value=1, max_value=6, label="Cuotas", required=False, initial=1)
    cuotas3 = forms.IntegerField(min_value=2, max_value=10, label="Cuotas", required=False, initial=1)
    tipo_pago = forms.ChoiceField(choices=[(0, 'Pago de Contado'), (1, 'Pago Prima ACH'), (2, 'Pago TDC'), (3, 'Otro')],
                                widget=forms.RadioSelect(), label="", required=True)
    guardar = forms.CharField(widget=forms.HiddenInput(), required=False)
