from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from polizas.forms import *
from datetime import date
from cotizador_acerta.views_mixins import LoginRequiredMixin
from polizas.models import *
from administrador.models import *
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.views.defaults import page_not_found
from django.contrib.humanize.templatetags.humanize import *
import json



class SolicitudPoliza(LoginRequiredMixin, generic.TemplateView):
    template_name = "polizas/solicitud.html"