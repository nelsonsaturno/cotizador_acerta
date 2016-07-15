from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import ListView
from darientSessions.models import *


class CorredorVendedorListView(ListView):
    model = DatosCorredor
    template_name = 'reportes/corredor_vendedor_list.html'

    def get_context_data(self, **kwargs):
        context = super(CorredorVendedorListView, self).get_context_data(**kwargs)
        vendedores = CorredorVendedor.objects.all()
        context['vendedores'] = vendedores
        return context