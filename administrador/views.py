#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from administrador.forms import *
from cotizador_acerta.views_mixins import LoginRequiredMixin
from administrador.models import *


class Dashboard(LoginRequiredMixin, generic.TemplateView):
    template_name = "administrador/dashboard.html"


class ListSexo(LoginRequiredMixin, generic.ListView):
    template_name = "administrador/list_sexo.html"
    model = Sexo
    context_object_name = 'sexos'


class AdminSexo(LoginRequiredMixin, generic.UpdateView):
    template_name = "administrador/sexo_form.html"
    model = Sexo
    form_class = SexoForm
    context_object_name = "sexo"
    success_url = 'list_sexo'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListHistorialTransito(LoginRequiredMixin, generic.ListView):
    template_name = "administrador/list_historial_transito.html"
    model = Historial_Transito
    context_object_name = 'historiales'


class AdminHistorialTransito(LoginRequiredMixin, generic.UpdateView):
    template_name = "administrador/historial_transito_form.html"
    model = Historial_Transito
    form_class = Historial_TransitoForm
    context_object_name = "historial"
    success_url = 'list_historial_transito'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)
