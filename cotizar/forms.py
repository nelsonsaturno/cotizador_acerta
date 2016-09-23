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
    
    provincia = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), ('PE', 'PE'), ('N', 'N'), ('E', 'E')], required=False)

    tipo = forms.ChoiceField(choices=[('PI', 'PI'), ('AV', 'AV')], required=False)

    campo_id_1 = forms.CharField(label="Campo 1", required=False, localize=True, max_length=3)

    campo_id_2 = forms.CharField(label="Campo 2", required=False, localize=True, max_length=4)

    identificacion = forms.CharField(label="Numero de Pasaporte", required=False)


    class Meta:
        model = ConductorVehiculo
        exclude = ['corredor', ]

        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'identificacion': 'Número de Pasaporte',
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
            'provincia': 'Provincia',
            'tipo': 'tipo',
            'campo_id_1': 'campo_id_1',
            'campo_id_2': 'campo_id_2',
        }
        widgets = {
            'marca': forms.Select(attrs={'class': 'select2'}),
            'modelo': forms.Select(attrs={'class': 'select2'}),
            'historial_transito': forms.Select(
                choices=[
                    (0, "0"), (1, "1"), (2, "2"), (3, "3"),
                    (4, "4"), (5, "5"), (6, "6"), (7, "7"),
                    (8, "8")
                ]
            ),
            'campo_id_1': forms.CharField(max_length=3)
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
        tipo_id = self.cleaned_data['tipo_id']
        campo_id_1 = self.cleaned_data['campo_id_1']
        campo_id_2 = self.cleaned_data['campo_id_2']
        if tipo_id == '0':
            print campo_id_1, 'hola'
            if campo_id_1 == '':
                raise forms.ValidationError(u'Este campo es requerido.')
            if campo_id_2 == '':
                raise forms.ValidationError(u'Este campo es requerido.')
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
        if self.cleaned_data['tipo_id'] == 0:
            conductor.tipo_id = 'cedula'
        else:
            conductor.tipo_id = 'pasaporte'
        if commit:
            conductor.save()
            return conductor
        else:
            return conductor


class CotizacionUpdateForm(forms.Form):

    cuotas = forms.ChoiceField(
        choices=(
            (1, "1"), (2, "2"), (3, "3"),
            (4, "4"), (5, "5"), (6, "6"),
            (7, "7"), (8, "8"), (9, "9"),
            (10, "10")
        ),
        label="Cuotas", required=False
    )
    cuotas2 = forms.ChoiceField(
        choices=(
            (1, "1"), (2, "2"), (3, "3"),
            (4, "4"), (5, "5"), (6, "6")
        ),
        label="Cuotas", required=False
    )
    cuotas3 = forms.ChoiceField(
        choices=(
            (2, "2"), (3, "3"),
            (4, "4"), (5, "5"), (6, "6"),
            (7, "7"), (8, "8"), (9, "9"),
            (10, "10")
        ),
        label="Cuotas", required=False,
    )
    tipo_pago = forms.ChoiceField(
        choices=[
            (0, 'Pago de Contado'),
            (1, 'Pago Prima ACH'),
            (2, 'Pago TCR'),
            (3, 'Otro')
        ],
        widget=forms.RadioSelect(),
        label="", required=True
    )
    guardar = forms.CharField(widget=forms.HiddenInput(), required=False)
