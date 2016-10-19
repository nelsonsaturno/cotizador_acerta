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
from django.views.defaults import page_not_found

from django.template import RequestContext
import ho.pisa as pisa
# from django.template.loader import render_to_string
# from django.template import RequestContext
# import ho.pisa as pisa
import cStringIO as StringIO
import cgi
import os

from num2words import num2words

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
            if solicitudes.last() == None:
                new_pk = 1
            else:
                new_pk = int(solicitudes.last().pk) + 1
        context['new_pk'] = new_pk
        cot = Cotizacion.objects.get(pk=kwargs['pk'])
        context['cotizacion'] = cot
        user = User.objects.get(username=cot.corredor)
        if user.groups.first().name != 'super_admin'\
           and user.groups.first().name != 'admin':
            if user.groups.first().name == 'corredor':
                context['corredor_pol'] = DatosCorredor.objects.get(user=user)
            else:
                vendedor = CorredorVendedor.objects.get(vendedor=user)
                context['corredor_pol'] = DatosCorredor.objects.get(user=vendedor.corredor)

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
            if user.groups.first().name == 'corredor':
                corredor = DatosCorredor.objects.get(user=user)
            else:
                vendedor = CorredorVendedor.objects.get(vendedor=user)
                corredor = DatosCorredor.objects.get(user=vendedor.corredor)
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
            extra_cliente.tipo = TipoVehiculo.objects.get(descrip=request.POST['tipo_vehiculo'])
            extra_cliente.save()
            conductor = [request.POST.get('nombre_conductor','n/a'),
                         request.POST.get('id_conductor','n/a')]
            if conductor[0] == 'n/a':
                conductor[0] = cotizacion.conductor.nombre + ' ' + cotizacion.conductor.apellido
            if conductor[1] == 'n/a':
                conductor[1] = cotizacion.conductor.identificacion

            conductor2 = [request.POST.get('nombre_conductor2','n/a'),
                         request.POST.get('id_conductor2','n/a')]
            if conductor2[0] == 'n/a':
                conductor2[0] = cotizacion.conductor2.nombre + ' ' + cotizacion.conductor2.apellido
            if conductor2[1] == 'n/a':
                conductor2[1] = cotizacion.conductor2.identificacion

            conductor3 = [request.POST.get('nombre_conductor3','n/a'),
                         request.POST.get('id_conductor3','n/a')]
            if conductor3[0] == 'n/a':
                conductor3[0] = cotizacion.conductor3.nombre + ' ' + cotizacion.conductor3.apellido
            if conductor3[1] == 'n/a':
                conductor3[1] = cotizacion.conductor3.identificacion

            responsable = [request.POST.get('nombre_responsable','n/a'),
                         request.POST.get('id_responsable','n/a')]
            if responsable[0] == 'n/a':
                responsable[0] = cotizacion.conductor.nombre + ' ' + cotizacion.conductor.apellido
            if responsable[1] == 'n/a':
                responsable[1] = cotizacion.conductor.identificacion


            tipo_id_conductor = form.cleaned_data['tipo_id_conductor']
            if tipo_id_conductor == '0':
                provincia_1 = form.cleaned_data['provincia_1']
                tipo_1 = form.cleaned_data['tipo_1']
                campo_id_1_1 = form.cleaned_data['campo_id_1_1']
                campo_id_2_1 = form.cleaned_data['campo_id_2_1']
                if str(provincia_1) == 'E':
                    cedula = str(provincia_1) + '-' + str(campo_id_1_1) + '-' + str(campo_id_2_1)
                else:
                    cedula = str(provincia_1) + '-' + str(tipo_1) + '-' + str(campo_id_1_1) + '-' + str(campo_id_2_1)
                conductor[1] = cedula
            else:
                conductor[1] = form.cleaned_data['id_conductor']


            tipo_id_conductor2 = form.cleaned_data['tipo_id_conductor2']
            if tipo_id_conductor2 == '0':
                provincia_2 = form.cleaned_data['provincia_2']
                tipo_2 = form.cleaned_data['tipo_2']
                campo_id_1_2 = form.cleaned_data['campo_id_1_2']
                campo_id_2_2 = form.cleaned_data['campo_id_2_2']
                if str(provincia_2) == 'E':
                    cedula = str(provincia_2) + '-' + str(campo_id_1_2) + '-' + str(campo_id_2_2)
                else:
                    cedula = str(provincia_2) + '-' + str(tipo_2) + '-' + str(campo_id_1_2) + '-' + str(campo_id_2_2)
                conductor2[1] = cedula
            else:
                conductor2[1] = form.cleaned_data['id_conductor2']

            tipo_id_conductor3 = form.cleaned_data['tipo_id_conductor3']
            if tipo_id_conductor3 == '0':
                provincia_3 = form.cleaned_data['provincia_3']
                tipo_3 = form.cleaned_data['tipo_3']
                campo_id_1_3 = form.cleaned_data['campo_id_1_3']
                campo_id_2_3 = form.cleaned_data['campo_id_2_3']
                if str(provincia_3) == 'E':
                    cedula = str(provincia_3) + '-' + str(campo_id_1_3) + '-' + str(campo_id_2_3)
                else:
                    cedula = str(provincia_3) + '-' + str(tipo_3) + '-' + str(campo_id_1_3) + '-' + str(campo_id_2_3)
                conductor3[1] = cedula
            else:
                conductor3[1] = form.cleaned_data['id_conductor3']

            tipo_id_responsable = form.cleaned_data['tipo_id_responsable']
            if tipo_id_responsable == '0':
                provincia_resp = form.cleaned_data['provincia_resp']
                tipo_resp = form.cleaned_data['tipo_resp']
                campo_id_1_resp = form.cleaned_data['campo_id_1_resp']
                cedula = str(provincia_resp) + '-' + str(tipo_resp) + '-' + str(campo_id_1_resp)
                campo_id_2_resp = form.cleaned_data['campo_id_2_resp']
                if provincia_resp <> 'E':
                    cedula = cedula + '-' + str(campo_id_2_resp)
                else:
                    cedula = str(provincia_1) + '-' + str(campo_id_1_resp) + '-' + str(campo_id_2_resp)
                responsable[1] = cedula
            else:
                responsable[1] = form.cleaned_data['id_responsable']


            date_desde = request.POST['valido_desde'].split('-')
            new_date_desde = str(date_desde[2]) +'-'+str(date_desde[1]) +'-'+ str(date_desde[0])
            anio_date_hasta = int(str(date_desde[2])) + 1
            new_date_hasta = str(anio_date_hasta) +'-'+str(date_desde[1]) +'-'+ str(date_desde[0])

            # Asegurado
            tipo_acreedor = form.cleaned_data['tipo_acreedor_leasing']
            if tipo_acreedor == 1:
                asegurado = cotizacion.conductor.nombre + ' ' + cotizacion.conductor.apellido
                id_asegurado = cotizacion.conductor.identificacion
            else:
                asegurado = form.cleaned_data['acreedor_leasing']
                id_asegurado = 'N/A'

            solicitud = SolicitudPoliza(
                cotizacion=cotizacion,
                asegurado=asegurado,
                id_asegurado=id_asegurado,
                nombre_conductor=conductor[0],
                id_conductor=conductor[1],
                nombre_conductor2=conductor2[0],
                id_conductor2=conductor2[1],
                nombre_conductor3=conductor3[0],
                id_conductor3=conductor3[1],
                vigencia_desde=new_date_desde,
                vigencia_hasta=new_date_hasta,
                firmador=cotizacion.conductor.nombre+' '+cotizacion.conductor.apellido+ '/ WEB',
                observaciones=request.POST.get('observaciones','N/A'),
                responsable=request.POST['responsable'],
                nombre_responsable=responsable[0],
                id_responsable=responsable[1],
                tipo_produccion=request.POST.get('tipo_produccion',''),
                tipo_suscripcion=request.POST.get('tipo_suscripcion',''),
                forma_facturacion=request.POST.get('forma_facturacion',''),
                renovacion_automatica=request.POST.get('renovacion',False),
                comision=request.POST.get('comision',False),
                def_comision=request.POST.get('def_comision',''),
                grupo_economico=request.POST.get('grupo_economico',''),
                aprobaciones=request.POST.get('aprobaciones',''),
                funcionario=request.POST.get('funcionario',''),
                cargo_funcionario=request.POST.get('cargo_funcionario',''),
                area_funcionario=request.POST.get('area_funcionario',''),
                otra_area=request.POST.get('otra_area',''),
                tipo_tdc=request.POST.get('tipo_tdc','N/A'),
                num_tdc=request.POST.get('num_tdc','N/A'),
                banco_tdc=request.POST.get('banco_tdc','N/A'),
                expiracion_tdc=request.POST.get('expiracion_tdc',date.today()),
                dia_cobro=request.POST.get('dia_cobro',''),
                cuenta_banco_num=request.POST.get('cuenta_banco_num',''),
                cuenta_banco_nombre=request.POST.get('cuenta_banco_nombre',''),
                cuenta_tipo=request.POST.get('cuenta_tipo',''),

                tipo='Solicitada'
            )


            if request.POST.get('aseguradoConductor') <> None:
                conductor[0] = solicitud.cotizacion.conductor.nombre + ' ' + solicitud.cotizacion.conductor.apellido
                conductor[1] = solicitud.cotizacion.conductor.identificacion

            solicitud.acreedor_leasing = Acreedores.objects.filter(nombre_acreedor=request.POST['acreedor_leasing'])[0]
            solicitud.tipo_acreedor_leasing = request.POST.get('tipo_acreedor_leasing')
            solicitud.id_conductor = conductor[1]
            solicitud.id_conductor2 = conductor2[1]
            solicitud.id_conductor3 = conductor3[1]
            solicitud.save()

            cotizacion.status = "Aprobada"
            cotizacion.save()
            subject = "Acerta Seguros - Aprobada la Cotizacion de Vehiculo"

            to_corredor = [request.user.email]
            from_email = request.user.email
            valor_vehiculo = intcomma(
                float("{0:.2f}".format(cotizacion.conductor.valor + 0.001)))
            prima_lesiones = intcomma(
                float("{0:.2f}".format(cotizacion.prima_lesiones)))
            prima_daniosProp = intcomma(
                float("{0:.2f}".format(cotizacion.prima_daniosProp)))
            prima_gastosMedicos = intcomma(
                float("{0:.2f}".format(cotizacion.prima_gastosMedicos)))
            colision_vuelco = intcomma(
                float("{0:.2f}".format(cotizacion.colision_vuelco)))
            prima_colisionVuelco = intcomma(
                float("{0:.2f}".format(cotizacion.prima_colisionVuelco)))
            otros_danios = intcomma(
                float("{0:.2f}".format(cotizacion.otros_danios)))
            prima_otrosDanios = intcomma(
                float("{0:.2f}".format(cotizacion.prima_otrosDanios)))
            incendio_rayo = intcomma(
                float("{0:.2f}".format(cotizacion.incendio_rayo)))
            robo_hurto = intcomma(
                float("{0:.2f}".format(cotizacion.robo_hurto)))
            prima_importacion = intcomma(
                float("{0:.2f}".format(cotizacion.prima_importacion)))
            subtotal = intcomma(
                float("{0:.2f}".format(cotizacion.subtotal)))
            impuestos = intcomma(
                float("{0:.2f}".format(cotizacion.impuestos)))
            total = intcomma(
                float("{0:.2f}".format(cotizacion.total)))
            prima_pagoVisa = intcomma(
                float("{0:.2f}".format(cotizacion.prima_pagoVisa)))
            prima_contado = intcomma(
                float("{0:.2f}".format(cotizacion.prima_pagoContado)))
            pago = cotizacion.tipo_pago
            prima_endoso = intcomma(
                float("{0:.2f}".format(cotizacion.prima_endoso)))

            if valor_vehiculo[-2] == '.':
                valor_vehiculo = valor_vehiculo + '0'
            if prima_lesiones[-2] == '.':
                prima_lesiones = prima_lesiones + '0'
            if prima_daniosProp[-2] == '.':
                prima_daniosProp = prima_daniosProp + '0'
            if prima_gastosMedicos[-2] == '.':
                prima_gastosMedicos = prima_gastosMedicos + '0'
            if colision_vuelco[-2] == '.':
                colision_vuelco = colision_vuelco + '0'
            if prima_colisionVuelco[-2] == '.':
                prima_colisionVuelco = prima_colisionVuelco + '0'
            if otros_danios[-2] == '.':
                otros_danios = otros_danios + '0'
            if prima_otrosDanios[-2] == '.':
                prima_otrosDanios = prima_otrosDanios + '0'
            if incendio_rayo[-2] == '.':
                incendio_rayo = incendio_rayo + '0'
            if robo_hurto[-2] == '.':
                robo_hurto = robo_hurto + '0'
            if prima_importacion[-2] == '.':
                prima_importacion = prima_importacion + '0'
            if subtotal[-2] == '.':
                subtotal = subtotal + '0'
            if impuestos[-2] == '.':
                im = impuestos + '0'
            if total[-2] == '.':
                total = total + '0'
            if prima_pagoVisa[-2] == '.':
                prima_pagoVisa = prima_pagoVisa + '0'
            if prima_contado[-2] == '.':
                prima_contado = prima_contado + '0'
            if prima_endoso[-2] == '.':
                prima_endoso = prima_endoso + '0'

            ctx = {
                'cotizacion': cotizacion,
                'valor_vehiculo': valor_vehiculo,
                'prima_lesiones': prima_lesiones,
                'prima_daniosProp': prima_daniosProp,
                'prima_gastosMedicos': prima_gastosMedicos,
                'colision_vuelco': colision_vuelco,
                'prima_colisionVuelco': prima_colisionVuelco,
                'otros_danios': otros_danios,
                'prima_otrosDanios': prima_otrosDanios,
                'incendio_rayo': incendio_rayo,
                'robo_hurto': robo_hurto,
                'prima_importacion': prima_importacion,
                'subtotal': subtotal,
                'impuestos': impuestos,
                'total': total,
                'prima_pagoVisa': prima_pagoVisa,
                'prima_contado': prima_contado,
                'tipo_pago': pago,
                'prima_endoso': prima_endoso,
            }

            # Correo Corredor
            message_corredor = get_template('cotizar/email_corredores.html')\
                .render(Context(ctx))
            msg = EmailMessage(subject,
                               message_corredor,
                               to=to_corredor)
            msg.content_subtype = 'html'
            msg.send()
            admins = ['jgutierrez@acertaseguros.com', 'ylezcano@acertaseguros.com']
            msg = EmailMessage(subject,
                               message_corredor,
                               to=admins)
            msg.content_subtype = 'html'
            msg.send()
            return HttpResponseRedirect(reverse_lazy('confirmar-solicitud', kwargs={'pk': solicitud.pk}))
        else:
            return render(
                request,
                self.template_name,
                {
                    'form': form,
                    'cotizacion': cotizacion,
                    'corredor_pol': corredor,
                }
            )


class ConfirmacionPago(generic.TemplateView):
    template_name = "polizas/confirmacion_pago.html"


class PagoTarjeta(generic.FormView):
    form_class = PagoForm
    template_name = "polizas/pago.html"
    success_url = reverse_lazy('confirmacion_pago')


class GeneracionPDFPolizas(LoginRequiredMixin, generic.CreateView):
    model = SolicitudPoliza
    template_name = 'polizas/pdf_personaNatural.html'

    def get(self, request, *args, **kwargs):

        solicitud = SolicitudPoliza.objects.get(pk=kwargs['pk'])
        datos_extra = ExtraDatosCliente.objects.get(
            conductor=solicitud.cotizacion.conductor)
        corredor = DatosCorredor.objects.get(
            user=solicitud.cotizacion.corredor)
        context = Context({'pagesize': 'letter'})
        context['solicitud'] = solicitud
        context['cotizacion'] = solicitud.cotizacion
        context['conductor1'] = solicitud.cotizacion.conductor
        context['conductor2'] = datos_extra
        context['corredor'] = corredor
        context['time'] = datetime.now()
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
        corredor = DatosCorredor.objects.get(
            user=solicitud.cotizacion.corredor)
        mylist = []
        today = date.today()
        mylist.append(today)
        context = Context({'pagesize': 'letter'})
        convert_date =  datetime.strptime(datos_extra.juridico_fecha_constitucion,'%Y-%m-%d')
        context['convert_fecha_const'] = convert_date.strftime('%d %b, %Y')
        context['solicitud'] = solicitud
        context['cotizacion'] = solicitud.cotizacion
        context['conductor1'] = solicitud.cotizacion.conductor
        context['conductor2'] = datos_extra
        context['corredor'] = corredor
        context['time'] = mylist[0]
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
        if poliza.tipo == 'Emitida':
            return page_not_found(request)
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
        user = User.objects.get(username=solicitud.cotizacion.corredor)
        poliza_corredor = PolizasCorredor.objects.filter(user=user)
        poliza_corredor = poliza_corredor.first()
        if not poliza_corredor:
            return page_not_found(request)
        corredor = ''

        if ((request.user.groups.first().name != "super_admin")\

           and (request.user.groups.first().name != "admin")):
            if request.user.groups.first().name == 'corredor':
                corredor = DatosCorredor.objects.get(user=request.user)
            else:
                vendedor = CorredorVendedor.objects.get(vendedor=user)
                corredor = DatosCorredor.objects.get(user=vendedor.corredor)
        inicial = request.user.first_name[0]
        etiqueta_corredor = str(inicial) + str(request.user.last_name)
        etiqueta_corredor = etiqueta_corredor.upper()
        extra_cliente = ExtraDatosCliente.objects.filter(conductor=cotizacion.conductor)
        if extra_cliente.first():
            extra_cliente = extra_cliente.first()
        else:
            extra_cliente = ''

        lesiones_corporales = cotizacion.lesiones_corporales.split('/')
        gastos_medicos = cotizacion.gastos_medicos.split('/')
        muerte_accidental = cotizacion.muerte_accidental.split('/')
        fecha = datetime.now()

        if fecha.month == 1:
            mes = 'enero'
        elif fecha.month == 2:
            mes = 'febrero'
        elif fecha.month == 3:
            mes = 'marzo'
        elif fecha.month == 4:
            mes = 'abril'
        elif fecha.month == 5:
            mes = 'mayo'
        elif fecha.month == 6:
            mes = 'junio'
        elif fecha.month == 7:
            mes = 'julio'
        elif fecha.month == 8:
            mes = 'agosto'
        elif fecha.month == 9:
            mes = 'septiembre'
        elif fecha.month == 10:
            mes = 'octubre'
        elif fecha.month == 11:
            mes = 'noviembre'
        elif fecha.month == 12:
            mes = 'diciembre'

        subtotal = cotizacion.subtotal
        impuestos = float("{0:.2f}".format(subtotal * 0.06))
        if solicitud.cotizacion.tipo_pago == 'Contado':
            conducto = 'CONTADO'
            subtotal = float("{0:.2f}".format(subtotal - (subtotal * 0.10)))
            impuestos = float("{0:.2f}".format(subtotal * 0.06))
            descuento =  cotizacion.subtotal - subtotal
            total = cotizacion.prima_pagoContado
        elif solicitud.cotizacion.tipo_pago == 'Visa':
            conducto = 'TARJETAS DE CREDITO'
            subtotal = float("{0:.2f}".format(subtotal - (subtotal * 0.05)))
            impuestos = float("{0:.2f}".format(subtotal * 0.06))
            descuento =  cotizacion.subtotal - subtotal
            total = cotizacion.prima_pagoVisa
        elif solicitud.cotizacion.tipo_pago == 'ACH':
            conducto = 'ACH'
            subtotal = float("{0:.2f}".format(subtotal - (subtotal * 0.05)))
            impuestos = float("{0:.2f}".format(subtotal * 0.06))
            descuento =  cotizacion.subtotal - subtotal
            total = cotizacion.prima_pagoVisa
        else:
            conducto = 'Otro'
            subtotal = cotizacion.subtotal
            descuento =  cotizacion.subtotal - subtotal
            impuestos = float("{0:.2f}".format(subtotal * 0.06))
            total = cotizacion.total

        tipo_pago = solicitud.cotizacion.tipo_pago

        endoso = solicitud.cotizacion.endoso.endoso.upper()

        monto_letras = num2words(total, lang='es')
        monto_letras = monto_letras.replace('punto','con')
        monto_letras = monto_letras.upper()

        tipo_cuenta = solicitud.cuenta_tipo
        tipo_cuenta = tipo_cuenta.upper()

        context = Context({'pagesize': 'letter',
                           'solicitud': solicitud,
                           'extra_cliente': extra_cliente,
                           'conductor': cotizacion.conductor,
                           'subtotal': subtotal,
                           'impuestos': impuestos,
                           'total': total,
                           'lesiones_corporales': lesiones_corporales,
                           'gastos_medicos': gastos_medicos,
                           'muerte_accidental': muerte_accidental,
                           'fecha':fecha,
                           'corredor': corredor,
                           'etiqueta_corredor': etiqueta_corredor,
                           'extra_cliente': extra_cliente,
                           'conducto': conducto,
                           'mes': mes,
                           'endoso': endoso,
                           'descuento': descuento,
                           'monto_letras': monto_letras,
                           'tipo_cuenta': tipo_cuenta,
                           'tipo_pago': tipo_pago})

        template_result = get_template('polizas/result_todas_pdf.html')
        html_result = template_result.render(context)
        template = get_template('polizas/emision_todas_pdf.html')
        html = template.render(context)
        template1 = get_template('polizas/emision_acreedor_asegurado_pdf.html')
        html1 = template1.render(context)
        template2 = get_template('polizas/emision_intermediario_pdf.html')
        html2 = template2.render(context)
        template3 = get_template('polizas/prueba_pdf.html')
        html3 = template3.render(context)

        file = open("polizas/" + 'emision_todas.pdf', "w+b")
        file1 = open("polizas/" + 'emision_intermediario.pdf', "w+b")
        file2 = open("polizas/" + 'emision_acreedor_asegurado.pdf', "w+b")
        file3 = open("polizas/" + 'emision_ACH.pdf', "w+b")
        result = StringIO.StringIO()
        links = lambda uri, rel: os.path.join(settings.STATIC_ROOT2, uri.replace(settings.STATIC_URL, ""))
        pdf = pisa.pisaDocument(StringIO.StringIO(html_result.encode("utf-8")), dest=result, encoding='UTF-8', link_callback=links)

        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), dest=file, encoding='UTF-8', link_callback=links)
        pdf1 = pisa.pisaDocument(StringIO.StringIO(html1.encode("utf-8")), dest=file1, encoding='UTF-8', link_callback=links)
        pdf2 = pisa.pisaDocument(StringIO.StringIO(html2.encode("utf-8")), dest=file2, encoding='UTF-8', link_callback=links)
        pdf3 = pisa.pisaDocument(StringIO.StringIO(html3.encode("utf-8")), dest=file3, encoding='UTF-8', link_callback=links)

        file.seek(0)
        pdf = file.read()
        file.close()

        file1.seek(0)
        pdf1 = file1.read()
        file1.close()

        file2.seek(0)
        pdf2 = file2.read()
        file2.close()

        file3.seek(0)
        pdf3 = file3.read()
        file3.close()

        if solicitud.tipo != 'Emitida':
            # Email enviado al cliente (asegurado)
            to = [solicitud.cotizacion.conductor.correo]
            from_email = request.user.email
            subject = 'Acerta Seguros - Emision Poliza'
            message = get_template('polizas/email_emision_poliza_cliente.html').render(context)
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.attach("polizas/emision_acreedor_asegurado.pdf",
                        pdf2,
                        'application/pdf')
            if solicitud.cotizacion.tipo_pago == 'ACH':
                msg.attach("polizas/emision_ACH.pdf",
                            pdf3,
                            'application/pdf')
            msg.send()

            # Email enviado al corredor
            to = [request.user.email]
            message = get_template('polizas/email_emision_poliza_corredor.html').render(context)
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.attach("polizas/emision_intermediario.pdf",
                        pdf1,
                        'application/pdf')
            if solicitud.cotizacion.tipo_pago == 'ACH':
                msg.attach("polizas/emision_ACH.pdf",
                            pdf3,
                            'application/pdf')
            msg.send()

            # Email enviado para notificacion de aprobacion
            to = ['jgutierrez@acertaseguros.com', 'ylezcano@acertaseguros.com']
            message = get_template('polizas/email_emision_poliza_notificacion.html').render(context)
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.attach("polizas/emision.pdf",
                        pdf,
                        'application/pdf')
            msg.send()


        return HttpResponse(result.getvalue(), 'application/pdf')



def SendEmailSolicitud(request, pk):
    subject = "Acerta Seguros - Solicitud Poliza"
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


def changeEmitida(request, pk):
    solicitud = SolicitudPoliza.objects.get(pk=pk)
    if solicitud.tipo == 'Emitida':
            return page_not_found(request)
    user = User.objects.get(username=solicitud.cotizacion.corredor)
    poliza_corredor = PolizasCorredor.objects.filter(user=user)
    poliza_corredor = poliza_corredor.first()
    if poliza_corredor:
        numero = poliza_corredor.polizas + poliza_corredor.polizas_desde
        poliza_corredor.polizas += 1
        poliza_corredor.save()
        solicitud.num = str(solicitud.cotizacion.corredor.pk) + str(numero)
        solicitud.tipo = 'Emitida'
        solicitud.save()
    return HttpResponseRedirect(
        reverse_lazy('polizas_list'))


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