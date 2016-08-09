#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from administrador.forms import *
from cotizador_acerta.views_mixins import *
from administrador.models import *
from cotizar.models import Modelo, Marca, MarcaHistory, ModeloHistory
from django.http import FileResponse, Http404


class Factores(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/dashboard.html"


class ListMarca(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_marca.html"
    model = Marca
    context_object_name = 'marcas'


class ListMarcaHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_marca_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        marca = Marca.objects.get(pk=kwargs['pk'])
        histories = MarcaHistory.objects.filter(prev_value=marca).order_by('-modified_at')
        context['histories'] = histories
        context['marca'] = marca
        return self.render_to_response(context)


class AdminMarca(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/marca_form.html"
    model = Marca
    form_class = MarcaForm
    context_object_name = "marca"
    success_url = 'list_marca'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = MarcaHistory(
            prev_value=self.object, nombre=form.cleaned_data['prev'], user=user
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListModelo(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_modelo.html"
    model = Modelo
    context_object_name = 'model'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None and
               hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(
                    _("Empty list and '%(class_name)s.allow_empty' is False.")
                    % {'class_name': self.__class__.__name__})
        context = self.get_context_data()
        marca = Marca.objects.get(pk=kwargs['pk'])
        modelos = Modelo.objects.filter(marca=marca)
        context['modelos'] = modelos
        context['marca'] = marca
        return self.render_to_response(context)


class ListModeloHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_modelo_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        modelo = Modelo.objects.get(pk=kwargs['pk'])
        histories = ModeloHistory.objects.filter(prev_value=modelo).order_by('-modified_at')
        context['histories'] = histories
        context['modelo'] = modelo
        return self.render_to_response(context)


class AdminModelo(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/modelo_form.html"
    model = Modelo
    form_class = ModeloForm
    context_object_name = "modelo"
    success_url = 'list_modelo'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = ModeloHistory(
            prev_value=self.object, marca=form.cleaned_data['marca'],
            user=user, nombre=form.cleaned_data['modelo'],
            descuento=form.cleaned_data['prev_d'],
            recargo=form.cleaned_data['prev_r']
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            self.success_url, kwargs={'pk': self.object.marca.pk})


class ListSexo(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_sexo.html"
    model = Sexo
    context_object_name = 'sexos'


class ListSexoHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_sexo_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        sexo = Sexo.objects.get(pk=kwargs['pk'])
        histories = SexoHistory.objects.filter(prev_value=sexo).order_by('-modified_at')
        context['histories'] = histories
        context['sexo'] = sexo
        return self.render_to_response(context)


class AdminSexo(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
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
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = SexoHistory(
            prev_value=self.object, factor=form.cleaned_data['prev'], user=user
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListHistorialTransito(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_historial_transito.html"
    model = Historial_Transito
    context_object_name = 'historiales'


class ListHistorialHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_transito_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        historial = Historial_Transito.objects.get(pk=kwargs['pk'])
        histories = HistorialHistory.objects.filter(prev_value=historial).order_by('-modified_at')
        context['histories'] = histories
        context['historial'] = historial
        return self.render_to_response(context)


class AdminHistorialTransito(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
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
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = HistorialHistory(
            prev_value=self.object, factor=form.cleaned_data['prev'],
            user=user, inferior=form.cleaned_data['prev_i'],
            superior=form.cleaned_data['prev_s']
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListEstadoCivil(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_estado_civil.html"
    model = Estado_Civil
    context_object_name = 'estados'


class ListEstadoCivilHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_estado_civil_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        estado_civil = Estado_Civil.objects.get(pk=kwargs['pk'])
        histories = EstadoCivilHistory.objects.filter(prev_value=estado_civil).order_by('-modified_at')
        context['histories'] = histories
        context['estado_civil'] = estado_civil
        return self.render_to_response(context)


class AdminEstadoCivil(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/estado_civil_form.html"
    model = Estado_Civil
    form_class = Estado_CivilForm
    context_object_name = "estado"
    success_url = 'list_estado_civil'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = EstadoCivilHistory(
            prev_value=self.object, factor=form.cleaned_data['prev'], user=user
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListValor(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_valor.html"
    model = Valor
    context_object_name = 'valores'


class ListValorHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_valor_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        valor = Valor.objects.get(pk=kwargs['pk'])
        histories = ValorHistory.objects.filter(prev_value=valor).order_by('-modified_at')
        context['histories'] = histories
        context['valor'] = valor
        return self.render_to_response(context)


class AdminValor(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/valor_form.html"
    model = Valor
    form_class = ValorForm
    context_object_name = "valor"
    success_url = 'list_valor'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = ValorHistory(
            prev_value=self.object, factor=form.cleaned_data['prev'],
            user=user, inferior=form.cleaned_data['prev_i'],
            superior=form.cleaned_data['prev_s']
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListAntiguedad(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_antiguedad.html"
    model = Antiguedad
    context_object_name = 'antiguedades'


class ListAntiguedadHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_antiguedad_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        antiguedad = Antiguedad.objects.get(pk=kwargs['pk'])
        histories = AntiguedadHistory.objects.filter(prev_value=antiguedad).order_by('-modified_at')
        context['histories'] = histories
        context['antiguedad'] = antiguedad
        return self.render_to_response(context)


class AdminAntiguedad(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/antiguedad_form.html"
    model = Antiguedad
    form_class = AntiguedadForm
    context_object_name = "antiguedad"
    success_url = 'list_antiguedad'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = AntiguedadHistory(
            prev_value=self.object, limite=form.cleaned_data['prev'],
            user=user, factor_menor=form.cleaned_data['prev_i'],
            factor_mayor=form.cleaned_data['prev_s']
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListEdad(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_edad.html"
    model = Edad
    context_object_name = 'edades'


class ListEdadHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_edad_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        edad = Edad.objects.get(pk=kwargs['pk'])
        histories = EdadHistory.objects.filter(prev_value=edad).order_by('-modified_at')
        context['histories'] = histories
        context['edad'] = edad
        return self.render_to_response(context)


class AdminEdad(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/edad_form.html"
    model = Edad
    form_class = EdadForm
    context_object_name = "edad"
    success_url = 'list_edad'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = EdadHistory(
            prev_value=self.object, factor=form.cleaned_data['prev'],
            user=user, inferior=form.cleaned_data['prev_i'],
            superior=form.cleaned_data['prev_s']
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListTiempoUso(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_tiempo_uso.html"
    model = Tiempo_Uso
    context_object_name = 'tiempos'


class ListTiempoUsoHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_tiempo_uso_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        tiempo = Tiempo_Uso.objects.get(pk=kwargs['pk'])
        histories = TiempoUsoHistory.objects.filter(prev_value=tiempo).order_by('-modified_at')
        context['histories'] = histories
        context['tiempo'] = tiempo
        return self.render_to_response(context)


class AdminTiempoUso(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/tiempo_uso_form.html"
    model = Tiempo_Uso
    form_class = Tiempo_UsoForm
    context_object_name = "tiempo"
    success_url = 'list_tiempo_uso'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = TiempoUsoHistory(
            prev_value=self.object, factor=form.cleaned_data['prev'], user=user
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListColision(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_colision.html"
    model = Colision
    context_object_name = 'colisiones'


class ListColisionHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_colision_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        colision = Colision.objects.get(pk=kwargs['pk'])
        histories = ColisionHistory.objects.filter(prev_value=colision).order_by('-modified_at')
        context['histories'] = histories
        context['colision'] = colision
        return self.render_to_response(context)


class AdminColision(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/colision_form.html"
    model = Colision
    form_class = ColisionForm
    context_object_name = "colision"
    success_url = 'list_colision'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = ColisionHistory(
            prev_value=self.object, factor=form.cleaned_data['prev'], user=user
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListImportacion(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_importacion.html"
    model = Importacion
    context_object_name = 'importaciones'


class ListImportacionHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_importacion_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        importacion = Importacion.objects.get(pk=kwargs['pk'])
        histories = ImportacionHistory.objects.filter(prev_value=importacion).order_by('-modified_at')
        context['histories'] = histories
        context['importacion'] = importacion
        return self.render_to_response(context)


class AdminImportacion(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/importacion_form.html"
    model = Importacion
    form_class = ImportacionForm
    context_object_name = "importacion"
    success_url = 'list_importacion'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = ImportacionHistory(
            prev_value=self.object, factor=form.cleaned_data['prev'], user=user
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListEndoso(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_endoso.html"
    model = Endoso
    context_object_name = 'endosos'


class ListEndosoHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_endoso_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        endoso = Endoso.objects.get(pk=kwargs['pk'])
        histories = EndosoHistory.objects.filter(prev_value=endoso).order_by('-modified_at')
        context['histories'] = histories
        context['endoso'] = endoso
        return self.render_to_response(context)


class AdminEndoso(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/endoso_form.html"
    model = Endoso
    form_class = EndosoForm
    context_object_name = "endoso"
    success_url = 'list_endoso'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = EndosoHistory(
            prev_value=self.object, endoso=form.cleaned_data['prev_n'],
            user=user, precio=form.cleaned_data['prev_p'],
            archivo=form.cleaned_data['prev_a']
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class CrearEndoso(LoginRequiredMixin, AdminRequiredMixin, generic.CreateView):
    template_name = "administrador/new_endoso_form.html"
    model = Endoso
    form_class = EndosoForm
    context_object_name = "endoso"
    success_url = 'list_endoso'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class DisplayPDFView(LoginRequiredMixin, AdminRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        endoso = Endoso.objects.get(pk=kwargs['pk'])
        return FileResponse(
            open(endoso.archivo.name, 'rb'), content_type='application/pdf')


class DisplayPDFHistoryView(LoginRequiredMixin, AdminRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        endoso = EndosoHistory.objects.get(pk=kwargs['pk'])
        return FileResponse(
            open(endoso.archivo, 'rb'), content_type='application/pdf')


class ListLesiones(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_lesiones.html"
    model = LesionesCorporales
    context_object_name = 'lesiones'


class ListLesionesHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_lesiones_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        lesion = LesionesCorporales.objects.get(pk=kwargs['pk'])
        histories = LesionesCorporalesHistory.objects.filter(prev_value=lesion).order_by('-modified_at')
        context['histories'] = histories
        context['lesion'] = lesion
        return self.render_to_response(context)


class AdminLesiones(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/lesiones_form.html"
    model = LesionesCorporales
    form_class = LesionesCorporalesForm
    context_object_name = "lesion"
    success_url = 'list_lesiones'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = LesionesCorporalesHistory(
            prev_value=self.object, factor=form.cleaned_data['prev'], user=user
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListDanios(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_danios.html"
    model = DaniosPropiedad
    context_object_name = 'danios'


class ListDaniosHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_danios_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        danio = DaniosPropiedad.objects.get(pk=kwargs['pk'])
        histories = DaniosHistory.objects.filter(prev_value=danio).order_by('-modified_at')
        context['histories'] = histories
        context['danio'] = danio
        return self.render_to_response(context)


class AdminDanios(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/danios_form.html"
    model = DaniosPropiedad
    form_class = DaniosPropiedadForm
    context_object_name = "danio"
    success_url = 'list_danios'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = DaniosHistory(
            prev_value=self.object, factor=form.cleaned_data['prev'], user=user
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class ListGastos(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = "administrador/list_gastos.html"
    model = GastosMedicos
    context_object_name = 'gastos'


class ListGastosHistory(LoginRequiredMixin, AdminRequiredMixin, generic.TemplateView):
    template_name = "administrador/list_gastos_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        gasto = GastosMedicos.objects.get(pk=kwargs['pk'])
        histories = GastosHistory.objects.filter(prev_value=gasto).order_by('-modified_at')
        context['histories'] = histories
        context['gasto'] = gasto
        return self.render_to_response(context)


class AdminGastos(LoginRequiredMixin, AdminRequiredMixin, generic.UpdateView):
    template_name = "administrador/gastos_form.html"
    model = GastosMedicos
    form_class = GastosMedicosForm
    context_object_name = "gasto"
    success_url = 'list_gastos'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(pk=form.cleaned_data['user'])
        historial = GastosHistory(
            prev_value=self.object, factor=form.cleaned_data['prev'], user=user
        )
        historial.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url)
