# from django.shortcuts import render
from django.views.generic import ListView
from darientSessions.models import DatosCorredor


class CorredorListView(ListView):
    model = DatosCorredor
    template_name = 'reportes/corredor_list.html'
