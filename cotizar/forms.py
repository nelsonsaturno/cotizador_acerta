#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from cotizar.models import *


class ConductorVehiculoForm(forms.ModelForm):

    tipo_id = forms.ChoiceField(choices=[(0, 'Cédula'), (1, 'Pasaporte')],
                                widget=forms.RadioSelect(), label="")

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

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(email=email).exclude(username=username).count() != 0:
    #         raise forms.ValidationError(u'Email addresses must be unique.')
    #     return email

    def save(self, commit=True):
        conductor = super(ConductorVehiculoForm, self).save(commit=False)
        if commit:
            conductor.save()
            return conductor
        else:
            return conductor


class CotizacionUpdateForm(forms.Form):

    cuotas = forms.IntegerField(min_value=1, max_value=10, label="Cuotas")
