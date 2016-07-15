from django.shortcuts import render_to_response
from django.views.generic import *
from cotizador_acerta.views_mixins import LoginRequiredMixin
from darientSessions.models import *
from cotizar.models import *


class CorredorVendedorListView(LoginRequiredMixin, ListView):
    model = DatosCorredor
    template_name = 'reportes/corredor_vendedor_list.html'

    def get_context_data(self, **kwargs):
        context = super(
            CorredorVendedorListView, self).get_context_data(**kwargs)
        vendedores = CorredorVendedor.objects.all()
        context['vendedores'] = vendedores
        return context


class CorredorVendedorDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/corredor_detail.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = User.objects.get(pk=kwargs['id'])
        context['user'] = user
        if user.groups.first().name == 'corredor':
            context['corredor'] = DatosCorredor.objects.get(user=user)
        cotizaciones = Cotizacion.objects.filter(corredor=user)
        context['cotizaciones'] = cotizaciones
        return self.render_to_response(context)

