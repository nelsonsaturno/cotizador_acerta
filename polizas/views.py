from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from polizas.forms import *
from datetime import date
from cotizador_acerta.views_mixins import LoginRequiredMixin
from polizas.models import *
from cotizar.models import *
from darientSessions.models import *
from administrador.models import *
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.views.defaults import page_not_found
from django.contrib.humanize.templatetags.humanize import *
import xhtml2pdf
from xhtml2pdf import pisa
import json
from easy_pdf.views import PDFTemplateView

class SolicitudPoliza(LoginRequiredMixin, generic.CreateView):
    template_name = "polizas/solicitud.html"
    form_class = SolicitudClienteForm
    model = SolicitudPoliza

    def form_valid(self, form):

        ########################################################
        # Metodo a ejecutarse luego de que el formulario es 
        # completado y valido. Renderiza el PDF.
        ########################################################

        context = Context({'pagesize':'letter'}) 
        template = get_template('polizas/prueba_pdf.html')
        html  = template.render(context)

        file = open("polizas/"+'prueba.pdf', "w+b")
        pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
            encoding='utf-8')

        file.seek(0)
        pdf = file.read()
        file.close()
   
        return HttpResponse(pdf, 'application/pdf')
        


    def get(self, request, *args, **kwargs):

        self.object = None
        context = self.get_context_data(**kwargs)
        cot = Cotizacion.objects.get(pk=kwargs['pk'])
        context['cotizacion'] = cot
        user = User.objects.get(username=cot.corredor)
        if user.groups.first() != 'super_admin' and user.groups.first() != 'admin':
            pass
            #passcontext['corredor_pol'] = DatosCorredor.objects.get(user=user)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Insert the form into the context dict.
        """
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(SolicitudPoliza, self).get_context_data(**kwargs)


class ConfirmacionPago(generic.TemplateView):
    template_name = "polizas/confirmacion_pago.html"


class PagoTarjeta(generic.FormView):
    form_class = PagoForm
    template_name = "polizas/pago.html"
    success_url = reverse_lazy('confirmacion_pago')


########################################################
#Vistas de prueba
########################################################

class Test(generic.TemplateView):
    template_name = "polizas/generacion_PDF.html"

class GeneracionPDF(LoginRequiredMixin, generic.CreateView):
    model = SolicitudPoliza
    template_name = 'polizas/prueba_pdf.html'

    def get(self, request, *args, **kwargs):

        context = Context({'pagesize':'letter'}) 
        template = get_template('polizas/prueba_pdf.html')
        html  = template.render(context)

        file = open("polizas/"+'prueba.pdf', "w+b")
        pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
            encoding='utf-8')

        file.seek(0)
        pdf = file.read()
        file.close()
   
        return HttpResponse(pdf, 'application/pdf')
        


class HelloPDFView(PDFTemplateView):
    template_name = "polizas/pdf_personaNatural.html"
