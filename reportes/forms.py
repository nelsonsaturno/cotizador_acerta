#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from datetime import *
from bootstrap3_datetime.widgets import DateTimePicker


class DateCotizationForm(forms.Form):
    start_date = forms.DateField(
        label='Fecha inicial', required=True,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    end_date = forms.DateField(
        label='Fecha final', required=True,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))


class ReportErrorForm(forms.Form):
    imagen = forms.ImageField(label='Captura de pantalla', required=False)
    descripcion = forms.CharField(
        label='Descripción del error',
        widget=forms.Textarea()
    )
    email = forms.EmailField(required=True, widget=forms.HiddenInput())
