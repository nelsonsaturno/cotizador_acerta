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
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.views.defaults import page_not_found
from django.contrib.humanize.templatetags.humanize import *
import json


class SolicitudPolizaView(LoginRequiredMixin, generic.CreateView):
    template_name = "polizas/solicitud.html"
    form_class = SolicitudClienteForm
    model = SolicitudPoliza

    def get(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data(**kwargs)
        cot = Cotizacion.objects.get(pk=kwargs['pk'])
        context['cotizacion'] = cot
        user = User.objects.get(username=cot.corredor)
        if user.groups.first().name != 'super_admin'\
           and user.groups.first().name != 'admin':
            context['corredor_pol'] = DatosCorredor.objects.get(user=user)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Insert the form into the context dict.
        """
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(SolicitudPolizaView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = SolicitudClienteForm(request.POST)
        cotizacion = Cotizacion.objects.get(pk=kwargs['pk'])
        user = User.objects.get(username=cotizacion.corredor)
        if user.groups.first().name != 'super_admin'\
           and user.groups.first().name != 'admin':
            corredor = DatosCorredor.objects.get(user=user)
        else:
            corredor = ''
        if form.is_valid():
            extra_cliente = form.save()
            ref1 = Referencia(
                nombre=request.POST['nom_ref_personal'],
                actividad=request.POST['actividad_ref_personal'],
                relacion=request.POST['relacion_ref_personal'],
                telefono=request.POST['telefono_ref_personal']
            )
            ref2 = Referencia(
                nombre=request.POST['nom_ref_bancaria'],
                actividad=request.POST['actividad_ref_bancaria'],
                relacion=request.POST['relacion_ref_bancaria'],
                telefono=request.POST['telefono_ref_bancaria']
            )
            ref3 = Referencia(
                nombre=request.POST['nom_ref_comercial'],
                actividad=request.POST['actividad_ref_comercial'],
                relacion=request.POST['relacion_ref_comercial'],
                telefono=request.POST['telefono_ref_comercial']
            )
            ref1.save()
            ref2.save()
            ref3.save()
            extra_cliente.ref_personal = ref1
            extra_cliente.ref_bancaria = ref2
            extra_cliente.ref_comercial = ref3
            extra_cliente.conductor = cotizacion.conductor
            extra_cliente.save()

            solicitud = SolicitudPoliza(
                cotizacion=cotizacion,
                nombre_conductor=request.POST['nombre_conductor'],
                id_conductor=request.POST['id_conductor'],
                vigencia_desde=request.POST['valido_desde'],
                vigencia_hasta=request.POST['valido_hasta'],
                acreedor=request.POST['acreedor'],
                leasing=request.POST['leasing'],
                firmador=request.POST['firmador'],
                observaciones=request.POST['observaciones'],
                responsable=request.POST['responsable'],
                nombre_responsable=request.POST['nombre_responsable'],
                id_responsable=request.POST['id_responsable'],
                tipo_produccion=request.POST['tipo_produccion'],
                tipo_suscripcion=request.POST['tipo_suscripcion'],
                forma_facturacion=request.POST['forma_facturacion'],
                renovacion_automatica=request.POST['renovacion'],
                comision=request.POST['comision'],
                def_comision=request.POST['def_comision'],
                grupo_economico=request.POST['grupo_economico'],
                aprobaciones=request.POST['aprobaciones'],
                funcionario=request.POST['funcionario'],
                cargo_funcionario=request.POST['cargo_funcionario'],
                area_funcionario=request.POST['area_funcionario'],
                otra_area=request.POST['otra_area'],
                tipo_tdc=request.POST.get('tipo_tdc',''),
                num_tdc=request.POST.get('num_tdc',''),
                banco_tdc=request.POST.get('banco_tdc',''),
                expiracion_tdc=request.POST.get('expiracion_tdc',date.today()),
                dia_pago=request.POST['dia_pago']
            )
            solicitud.save()
            return HttpResponseRedirect(reverse_lazy('cotizaciones_list'))
        else:
            return render(request, self.template_name, {'form': form,'cotizacion': cotizacion, 'corredor_pol': corredor})


class DetallePoliza(LoginRequiredMixin, generic.TemplateView):
    template_name = "polizas/detalle_poliza.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        poliza = SolicitudPoliza.objects.get(pk=kwargs['pk'])
        user = User.objects.get(username=poliza.cotizacion.corredor)
        if user.groups.first().name != 'super_admin'\
           and user.groups.first().name != 'admin':
            corredor = DatosCorredor.objects.get(user=user)
            context['corredor'] = corredor
        context['poliza'] = poliza
        extra_datos = ExtraDatosCliente.objects.get(conductor=poliza.cotizacion.conductor)
        context['extra_datos'] = extra_datos
        return self.render_to_response(context)


class ConfirmacionPago(generic.TemplateView):
    template_name = "polizas/confirmacion_pago.html"


class PagoTarjeta(generic.FormView):
    form_class = PagoForm
    template_name = "polizas/pago.html"
    success_url = reverse_lazy('confirmacion_pago')
