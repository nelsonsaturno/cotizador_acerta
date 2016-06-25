#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from cotizar.models import *


class ConductorForm(forms.ModelForm):

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
            'telefono1': 'Teléfono 1',
            'telefono2': 'Teléfono 2',
            'historial_transito': 'Historial de Tránsito',
        }

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(email=email).exclude(username=username).count() != 0:
    #         raise forms.ValidationError(u'Email addresses must be unique.')
    #     return email

    def save(self, commit=True):
        conductor = super(ConductorForm, self).save(commit=False)
        if commit:
            conductor.save()
            return conductor
        else:
            return conductor


class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        exclude = ['conductor']

        # widgets = {
        #     'sexo': forms.widgets.Select(choices=('Masculino', 'Femenino')),
        #     'estado_civil': forms.widgets.Select(choices=('Soltero(a)', 'Casado(a)', 'Otro')),
        # }

        # labels = {
        #     'nombre': 'Nombre',
        #     'apellido': 'Apellido',
        #     'sexo': 'Sexo',
        #     'identificacion': 'Identificación',
        #     'estado_civil': 'Estado Civil',
        #     'correo': 'Correo',
        #     'telefono1': 'Teléfono 1',
        #     'telefono2': 'Teléfono 2',
        #     'historial_transito': 'Historial de Tránsito',
        # }

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(email=email).exclude(username=username).count() != 0:
    #         raise forms.ValidationError(u'Email addresses must be unique.')
    #     return email

    def save(self, commit=True):
        vehiculo = super(VehiculoForm, self).save(commit=False)
        return vehiculo


class CotizacionUpdateForm(forms.ModelForm):

    class Meta:
        model = Cotizacion
        exclude = ['conductor', 'vehiculo', 'corredor',]
