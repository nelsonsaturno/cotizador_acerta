from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from polizas.forms import *
from datetime import date, datetime
from cotizador_acerta.views_mixins import LoginRequiredMixin
from polizas.models import *
from cotizar.models import *
from darientSessions.models import *
from administrador.models import *
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib.humanize.templatetags.humanize import *
from xhtml2pdf import pisa
from easy_pdf.views import PDFTemplateView

from django.template import RequestContext
import ho.pisa as pisa
# from django.template.loader import render_to_string
# from django.template import RequestContext
# import ho.pisa as pisa
import cStringIO as StringIO
import cgi
import os

class SolicitudPolizaView(LoginRequiredMixin, generic.CreateView):
    template_name = "polizas/solicitud.html"
    form_class = SolicitudClienteForm
    model = SolicitudPoliza

    def form_valid(self, form):

        ########################################################
        # Metodo a ejecutarse luego de que el formulario es
        # completado y valido. Renderiza el PDF.
        ########################################################

        context = Context({'pagesize': 'letter'})
        template = get_template('polizas/prueba_pdf.html')
        html = template.render(context)

        file = open("polizas/" + 'prueba.pdf', "w+b")
        pisa.CreatePDF(
            html.encode('utf-8'),
            dest=file,
            encoding='utf-8'
        )

        file.seek(0)
        pdf = file.read()
        file.close()
        return HttpResponse(pdf, 'application/pdf')

    def get(self, request, *args, **kwargs):

        self.object = None
        context = self.get_context_data(**kwargs)
        solicitudes = SolicitudPoliza.objects.all()
        if solicitudes == []:
            new_pk = 1
        else:
            new_pk = int(solicitudes.last().pk) + 1
        context['new_pk'] = new_pk
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
            if request.POST.get('nom_ref_personal', '') != '':
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
            conductor = [request.POST.get('nombre_conductor','n/a'),
                         request.POST.get('id_conductor','n/a')]
            if conductor[0] == 'n/a':
                conductor[0] = cotizacion.conductor.nombre + ' ' + cotizacion.conductor.apellido
            if conductor[1] == 'n/a':
                conductor[1] = cotizacion.conductor.identificacion

            responsable = [request.POST.get('nombre_responsable','n/a'),
                         request.POST.get('id_responsable','n/a')]
            if responsable[0] == 'n/a':
                responsable[0] = cotizacion.conductor.nombre + ' ' + cotizacion.conductor.apellido
            if responsable[1] == 'n/a':
                responsable[1] = cotizacion.conductor.identificacion
            
            solicitud = SolicitudPoliza(
                cotizacion=cotizacion,
                nombre_conductor=conductor[0],
                id_conductor=conductor[1],
                vigencia_desde=request.POST['valido_desde'],
                vigencia_hasta=request.POST['valido_hasta'],
                acreedor=request.POST.get('acreedor','N/A'),
                leasing=request.POST.get('leasing','N/A'),
                firmador=request.POST['firmador'],
                observaciones=request.POST.get('observaciones','N/A'),
                responsable=request.POST['responsable'],
                nombre_responsable=responsable[0],
                id_responsable=responsable[1],
                tipo_produccion=request.POST['tipo_produccion'],
                tipo_suscripcion=request.POST['tipo_suscripcion'],
                forma_facturacion=request.POST['forma_facturacion'],
                renovacion_automatica=request.POST.get('renovacion',False),
                comision=request.POST.get('comision',False),
                def_comision=request.POST.get('def_comision','N/A'),
                grupo_economico=request.POST['grupo_economico'],
                aprobaciones=request.POST.get('aprobaciones','N/A'),
                funcionario=request.POST['funcionario'],
                cargo_funcionario=request.POST['cargo_funcionario'],
                area_funcionario=request.POST['area_funcionario'],
                otra_area=request.POST.get('otra_area','N/A'),
                tipo_tdc=request.POST.get('tipo_tdc','N/A'),
                num_tdc=request.POST.get('num_tdc','N/A'),
                banco_tdc=request.POST.get('banco_tdc','N/A'),
                expiracion_tdc=request.POST.get('expiracion_tdc',date.today()),
                dia_pago=request.POST['dia_pago'],
                tipo='Solicitada'
            )
            
            solicitud.save()
            return HttpResponseRedirect(reverse_lazy('confirmar-solicitud', kwargs={'pk': solicitud.pk}))
        else:
            return render(
                request,
                self.template_name,
                {
                    'form': form,
                    'cotizacion': cotizacion,
                    'corredor_pol': corredor
                }
            )


class ConfirmacionPago(generic.TemplateView):
    template_name = "polizas/confirmacion_pago.html"


class PagoTarjeta(generic.FormView):
    form_class = PagoForm
    template_name = "polizas/pago.html"
    success_url = reverse_lazy('confirmacion_pago')


########################################################
# Vistas de prueba
########################################################

class Test(generic.TemplateView):
    template_name = "polizas/generacion_PDF.html"


class GeneracionPDF(LoginRequiredMixin, generic.CreateView):
    model = SolicitudPoliza
    template_name = 'polizas/prueba_pdf.html'

    def get(self, request, *args, **kwargs):

        context = Context({'pagesize': 'letter'})
        template = get_template('polizas/prueba_pdf.html')
        html = template.render(context)

        file = open("polizas/" + 'prueba.pdf', "w+b")
        # pisa.CreatePDF(
        #     html.encode('utf-8'),
        #     dest=file,
        #     encoding='utf-8',
        #     base_url=request.build_absolute_uri(),
        # )
        

        #html  = render_to_string('polizas/prueba_pdf.html', { 'pagesize' : 'letter', }, context_instance=RequestContext(request))
        result = StringIO.StringIO()
        links = lambda uri, rel: os.path.join(settings.STATIC_ROOT2, uri.replace(settings.STATIC_URL, ""))
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, encoding='UTF-8', link_callback=links)

 
        if not pdf.err:
            return HttpResponse(result.getvalue(), 'application/pdf')
        return HttpResponse('Gremlins ate your pdf! %s' % cgi.escape(html))


        #return HttpResponse(pdf, 'application/pdf')

    def fetch_resources(uri, rel):
        import os.path
        from django.conf import settings
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

        return path


class GeneracionPDFPolizas(LoginRequiredMixin, generic.CreateView):
    model = SolicitudPoliza
    template_name = 'polizas/pdf_personaNatural.html'

    def get(self, request, *args, **kwargs):

        solicitud = SolicitudPoliza.objects.get(pk=kwargs['pk'])
        datos_extra = ExtraDatosCliente.objects.get(
            conductor=solicitud.cotizacion.conductor)
        context = Context({'pagesize': 'letter'})
        context['solicitud'] = solicitud
        context['cotizacion'] = solicitud.cotizacion
        context['conductor1'] = solicitud.cotizacion.conductor
        context['conductor2'] = datos_extra
        template = get_template('polizas/pdf_personaNatural.html')
        html = template.render(context)

        file = open("polizas/" + 'personaNatural.pdf', "w+b")
        pisa.CreatePDF(
            html.encode('utf-8'),
            dest=file,
            encoding='utf-8'
        )

        file.seek(0)
        pdf = file.read()
        file.close()

        return HttpResponse(pdf, 'application/pdf')


class HelloPDFView(PDFTemplateView):
    template_name = "polizas/pdf_personaNatural.html"


class GeneracionPDFPolizas(LoginRequiredMixin, generic.CreateView):
    model = SolicitudPoliza
    template_name = 'polizas/pdf_personaNatural.html'

    def get(self, request, *args, **kwargs):

        solicitud = SolicitudPoliza.objects.get(pk=kwargs['pk'])
        datos_extras = ExtraDatosCliente.objects.filter(
            conductor=solicitud.cotizacion.conductor)
        datos_extra = datos_extras.last()
        context = Context({'pagesize': 'letter'})
        context['solicitud'] = solicitud
        context['cotizacion'] = solicitud.cotizacion
        context['conductor1'] = solicitud.cotizacion.conductor
        context['conductor2'] = datos_extra
        template = get_template('polizas/pdf_personaNatural.html')
        html = template.render(context)

        file = open("polizas/" + 'personaNatural.pdf', "w+b")
        pisa.CreatePDF(
            html.encode('utf-8'),
            dest=file,
            encoding='utf-8'
        )

        file.seek(0)
        pdf = file.read()
        file.close()

        return HttpResponse(pdf, 'application/pdf')


class ConfirmarSolicitud(LoginRequiredMixin, generic.TemplateView):
    template_name = "polizas/confirmacion_solicitud.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        poliza = SolicitudPoliza.objects.get(pk=kwargs['pk'])
        user = User.objects.get(username=poliza.cotizacion.corredor)
        context['solicitud'] = poliza
        #extra_datos = ExtraDatosCliente.objects.get(conductor=poliza.cotizacion.conductor)
        #context['cliente'] = extra_datos
        return self.render_to_response(context)


class EmitirPoliza(LoginRequiredMixin, generic.CreateView):
    template_name = 'polizas/prueba_pdf.html'

    def get(self, request, *args, **kwargs):


        solicitud = SolicitudPoliza.objects.get(pk=kwargs['pk'])
        cotizacion = solicitud.cotizacion
        user = User.objects.get(username=cotizacion.corredor)
        if user.groups.first().name != 'super_admin'\
           and user.groups.first().name != 'admin':
            corredor = DatosCorredor.objects.get(user=user)
        else:
            corredor = ''
        #extra_cliente = ExtraDatosCliente.objects.get(conductor=cotizacion.conductor)
        extra_cliente = ''

        subtotal = cotizacion.subtotal - cotizacion.descuento
        lesiones_corporales = cotizacion.lesiones_corporales.split('/')
        gastos_medicos = cotizacion.gastos_medicos.split('/')
        muerte_accidental = cotizacion.muerte_accidental.split('/')
        fecha = datetime.now()

        context = Context({'pagesize': 'letter',
                           'solicitud': solicitud,
                           'extra_cliente': extra_cliente,
                           'conductor': cotizacion.conductor,
                           'subtotal': subtotal,
                           'lesiones_corporales': lesiones_corporales,
                           'gastos_medicos': gastos_medicos,
                           'muerte_accidental': muerte_accidental,
                           'fecha':fecha,
                           'corredor': corredor})
        template = get_template('polizas/prueba_pdf.html')
        html = template.render(context)

        file = open("polizas/" + 'prueba.pdf', "w+b")
        result = StringIO.StringIO()
        links = lambda uri, rel: os.path.join(settings.STATIC_ROOT2, uri.replace(settings.STATIC_URL, ""))
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), dest=result, encoding='UTF-8', link_callback=links)
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), dest=file, encoding='UTF-8', link_callback=links)

        file.seek(0)
        pdf = file.read()
        file.close()

        return HttpResponse(result.getvalue(), 'application/pdf')



def SendEmailSolicitud(request, pk):
    subject = "Acerta Seguros - Solicitud PEP"
    solicitud = SolicitudPoliza.objects.get(pk=pk)
    datos_extras = ExtraDatosCliente.objects.filter(
        conductor=solicitud.cotizacion.conductor)
    datos_extra = datos_extras.last()
    context = Context({'pagesize': 'letter'})
    context['solicitud'] = solicitud
    context['cotizacion'] = solicitud.cotizacion
    context['conductor1'] = solicitud.cotizacion.conductor
    context['conductor2'] = datos_extra
    template = get_template('polizas/pdf_personaNatural.html')
    html = template.render(context)

    file = open("polizas/" + 'personaNatural.pdf', "w+b")
    pisa.CreatePDF(
        html.encode('utf-8'),
        dest=file,
        encoding='utf-8'
    )

    file.seek(0)
    pdf = file.read()
    file.close()
    to = [solicitud.cotizacion.conductor.correo]
    from_email = request.user.email
    ctx = {
        'solicitud': solicitud
    }
    message = get_template('polizas/email_solicitud.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.attach("solicitud.pdf",
       pdf,
       'application/pdf')
    msg.send()
    return HttpResponseRedirect(
        reverse_lazy('polizas_list'))
