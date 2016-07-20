from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import *
from cotizador_acerta.views_mixins import *
from darientSessions.models import *
from cotizar.models import *
from django.contrib.auth.models import User
from django.views.defaults import page_not_found


class CorredorVendedorListView(LoginRequiredMixin,
                               GroupRequiredMixin, ListView):
    model = DatosCorredor
    template_name = 'reportes/corredor_vendedor_list.html'

    def get_context_data(self, **kwargs):
        context = super(
            CorredorVendedorListView, self).get_context_data(**kwargs)
        vendedores = CorredorVendedor.objects.all()
        context['vendedores'] = vendedores
        return context


class CorredorVendedorDetailView(LoginRequiredMixin,
                                 DetailRequiredMixin, TemplateView):
    template_name = 'reportes/corredor_detail.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        if request.user.groups.first().name == 'corredor':
            vendedor = CorredorVendedor.objects.filter(vendedor=user)
            if len(vendedor) == 0:
                return page_not_found(request)
            if vendedor[0].corredor.pk != request.user.pk:
                return page_not_found(request)
        context = self.get_context_data(**kwargs)
        context['usuario'] = user
        if user.groups.first().name == 'corredor':
            context['corredor'] = DatosCorredor.objects.get(user=user)
        cotizaciones = Cotizacion.objects.filter(corredor=user, is_active=True)
        num_cot = len(cotizaciones)
        context['cotizaciones'] = cotizaciones
        context['num_cot'] = num_cot
        return self.render_to_response(context)


class VendedorListView(LoginRequiredMixin, CorredorRequiredMixin, ListView):
    template_name = 'reportes/vendedor_list.html'
    model = User

    def get(self, request, *args, **kwargs):
        self.object_list = []
        context = super(
            VendedorListView, self).get_context_data(**kwargs)
        corredor = User.objects.get(pk=request.user.pk)
        vendedores = CorredorVendedor.objects.filter(corredor=corredor)
        context['vendedores'] = vendedores
        return self.render_to_response(context)


class CotizacionesListView(LoginRequiredMixin, ListView):
    template_name = 'reportes/cotizaciones_list.html'
    model = Cotizacion

    def get(self, request, *args, **kwargs):
        self.object_list = []
        context = super(
            CotizacionesListView, self).get_context_data(**kwargs)
        corredor = User.objects.get(pk=request.user.pk)
        cotizaciones = Cotizacion.objects.filter(corredor=corredor, is_active=True)
        context['cotizaciones'] = cotizaciones
        return self.render_to_response(context)


class CotizacionesDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/cotizacion_details.html'
    model = Cotizacion

    def get(self, request, *args, **kwargs):
        context = super(
            CotizacionesDetailView, self).get_context_data(**kwargs)
        cotizacion = Cotizacion.objects.get(pk=kwargs['pk'], is_active=True)
        if cotizacion.corredor.pk != request.user.pk:
            return page_not_found(request)
        context['cotizacion'] = cotizacion
        return self.render_to_response(context)


class DashboardView(LoginRequiredMixin,
                                 DetailRequiredMixin, TemplateView):
    template_name = 'reportes/dashboard.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        context = self.get_context_data(**kwargs)
        if request.user.groups.first().name == 'corredor':
            vendedor = CorredorVendedor.objects.filter(vendedor=user)
            if len(vendedor) == 0:
                return page_not_found(request)
            if vendedor[0].corredor.pk != request.user.pk:
                return page_not_found(request)
        elif request.user.groups.first().name == 'super_admin':
            corredores = DatosCorredor.objects.all()
            for corredor in corredores:
                cotizaciones = Cotizacion.objects.filter(
                    corredor=corredor.user, is_active=True)
                context[corredor.user.username] = len(cotizaciones)
            context['corredores'] = corredores
            vendedores = CorredorVendedor.objects.all()
            context['vendedores'] = vendedores
        context['usuario'] = user
        if user.groups.first().name == 'corredor':
            context['corredor'] = DatosCorredor.objects.get(user=user)
        cotizaciones = Cotizacion.objects.filter(corredor=user, is_active=True)

        num_cot = len(cotizaciones)
        context['cotizaciones'] = cotizaciones
        context['num_cot'] = num_cot
        return self.render_to_response(context)
