#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from datetime import *
from bootstrap3_datetime.widgets import DateTimePicker


class DateCotizationForm(forms.Form):
    start_date = forms.DateField(
        label='Fecha inicial',
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    end_date = forms.DateField(
        label='Fecha final',
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
