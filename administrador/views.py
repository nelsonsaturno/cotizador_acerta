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
    form_class = SexoForm
    model = Sexo
    success_url = 'list_sexo'

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        if form.is_valid():
            sexo = Sexo.objects.get(pk=kwargs['pk'])
            sexo.factor = float(request.POST['factor'])
            sexo.save()
            return HttpResponseRedirect(reverse_lazy(self.success_url))
        else:
            return self.form_invalid(form)
