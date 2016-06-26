#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from cotizar.models import *


class ConductorVehiculoForm(forms.ModelForm):

    class Meta:
        model = Conductor
        exclude = []

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


class CotizacionUpdateForm(forms.ModelForm):

    class Meta:
        model = Cotizacion
        exclude = ['conductor', 'vehiculo', 'corredor',]
