#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from administrador.models import *


class SexoForm(forms.ModelForm):

    class Meta:
        model = Sexo
        exclude = []

        labels = {
            'sexo': 'Sexo',
            'factor': 'Factor',
        }

    # def save(self, commit=True):
    #     sexo = super(SexoForm, self).save(commit=False)
    #     if commit:
    #         sexo.save()
    #         return sexo
    #     else:
    #         return sexo


class Estado_CivilForm(forms.ModelForm):

    class Meta:
        model = Estado_Civil
        exclude = []

        labels = {
            'estado_civil': 'Estado Civil',
            'factor': 'Factor',
        }

    def save(self, commit=True):
        estado_civil = super(Estado_CivilForm, self).save(commit=False)
        if commit:
            estado_civil.save()
            return estado_civil
        else:
            return estado_civil


class ValorForm(forms.ModelForm):

    class Meta:
        model = Valor
        exclude = []

        labels = {
            'inferior': 'Desde: (B./)',
            'superior': 'Hasta: (B./)',
            'factor': 'Factor',
        }

    def save(self, commit=True):
        valor = super(ValorForm, self).save(commit=False)
        if commit:
            valor.save()
            return valor
        else:
            return valor


class Historial_TransitoForm(forms.ModelForm):

    class Meta:
        model = Historial_Transito
        exclude = []

        labels = {
            'inferior': 'Desde: (Pts)',
            'superior': 'Hasta: (Pts)',
            'factor': 'Factor',
        }

    def save(self, commit=True):
        historial = super(Historial_TransitoForm, self).save(commit=False)
        if commit:
            historial.save()
            return historial
        else:
            return historial


class AntiguedadForm(forms.ModelForm):

    class Meta:
        model = Antiguedad
        exclude = []

        labels = {
            'limite': 'Mayor que/Menor o igual que: (Años)',
            'factor_mayor': 'Factor Mayor que',
            'factor_menor': 'Factor Menor o igual que',
        }

    def save(self, commit=True):
        antiguedad = super(AntiguedadForm, self).save(commit=False)
        if commit:
            antiguedad.save()
            return antiguedad
        else:
            return antiguedad


class EdadForm(forms.ModelForm):

    class Meta:
        model = Edad
        exclude = []

        labels = {
            'inferior': 'Desde: (Años)',
            'superior': 'Hasta: (Años)',
            'factor': 'Factor',
        }

    def save(self, commit=True):
        edad = super(EdadForm, self).save(commit=False)
        if commit:
            edad.save()
            return edad
        else:
            return edad


class Tiempo_UsoForm(forms.ModelForm):

    class Meta:
        model = Tiempo_Uso
        exclude = []

        labels = {
            'tiempo': 'Tiempo de Uso: (Años)',
            'factor': 'Factor',
        }

    def save(self, commit=True):
        tiempo = super(Tiempo_UsoForm, self).save(commit=False)
        if commit:
            tiempo.save()
            return tiempo
        else:
            return tiempo


class ColisionForm(forms.ModelForm):

    class Meta:
        model = Colision
        exclude = []

        labels = {
            'tiempo': 'Tiempo de Uso: (Años)',
            'factor': 'Factor',
        }

    def save(self, commit=True):
        tiempo = super(ColisionForm, self).save(commit=False)
        if commit:
            tiempo.save()
            return tiempo
        else:
            return tiempo


class ImportacionForm(forms.ModelForm):

    class Meta:
        model = Importacion
        exclude = []

        labels = {
            'factor': 'Factor',
        }

    def save(self, commit=True):
        importacion = super(ImportacionForm, self).save(commit=False)
        if commit:
            importacion.save()
            return importacion
        else:
            return importacion


class Acerta_PreferencialForm(forms.ModelForm):

    class Meta:
        model = Acerta_Preferencial
        exclude = []

        labels = {
            'factor': 'Factor',
        }

    def save(self, commit=True):
        preferencial = super(Acerta_PreferencialForm, self).save(commit=False)
        if commit:
            preferencial.save()
            return preferencial
        else:
            return preferencial
