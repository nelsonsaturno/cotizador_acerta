#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from datetime import *


class DateCotizationForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
