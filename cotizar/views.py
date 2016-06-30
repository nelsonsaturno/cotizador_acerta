#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from cotizar.forms import *
from datetime import date
from cotizador_acerta.views_mixins import LoginRequiredMixin
from cotizar.models import *
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
import json


class CotizarAhora(LoginRequiredMixin, generic.TemplateView):
    template_name = "cotizar/cotiza_ahora.html"


class Vehiculo(LoginRequiredMixin, generic.CreateView):
    template_name = "cotizar/vehiculo.html"
    form_class = ConductorVehiculoForm

    def crear_cotizacion(self, request, vehiculo):
        conductor = vehiculo
        if conductor.sexo == 'Masculino':
            sexo = 1.01
        else:
            sexo = 0.95

        if conductor.estado_civil == 'Soltero(a)':
            estado_civil = 1.09
        if conductor.estado_civil == 'Casado(a)':
            estado_civil = 0.97
        if conductor.estado_civil == 'Otro':
            estado_civil = 0.99
        if conductor.edad >= 30:
            estado_civil = 0.97

        if vehiculo.valor <= 17000:
            valor = 1.20
        elif (vehiculo.valor > 17000) and (vehiculo.valor <= 25000):
            valor = 1.10
        elif (vehiculo.valor > 25000) and (vehiculo.valor <= 70000):
            valor = 0.96
        else:
            valor = 0.99

        if conductor.historial_transito < 4:
            historial_transito = 1
        elif (conductor.historial_transito >= 4) and\
             (conductor.historial_transito <= 7):
            historial_transito = 1.10
        else:
            historial_transito = 1.20

        antig = date.today().year - vehiculo.anio

        if antig <= 3:
            antiguedad = 0.43
        else:
            antiguedad = 0.50

        if conductor.edad <= 25:
            edad = 1.10
        elif (conductor.edad >= 26) and (conductor.edad <= 65):
            edad = 0.98
        else:
            edad = 1.00

        desc_parametros = 1.00 -\
            (sexo * estado_civil * valor *
             historial_transito * antiguedad * edad)

        descuento = min(vehiculo.modelo.descuento, desc_parametros)
        descuento = float("{0:.2f}".format(descuento))

        if descuento < 0.3:
            descuento = 0.3
        elif descuento > 0.625:
            descuento = 0.625

        # lesiones_corporales = '25,000.00/50,000.00'
        # danios_propiedad = '50,000.00'
        # gastos_medicos = '2,000.00/10,000.00'
        if vehiculo.importacion_piezas:
            importa = True
            importacion_piezas = float(
                "{0:.2f}".format(vehiculo.valor * 0.0018))
        else:
            importa = False
            importacion_piezas = 0.00

        if (vehiculo.lesiones_corporales == '5,000.00/10,000.00'):
            base_lesiones = 30
        elif (vehiculo.lesiones_corporales == '10,000.00/20,000.00'):
            base_lesiones = 60
        elif (vehiculo.lesiones_corporales == '20,000.00/40,000.00'):
            base_lesiones = 75
        elif (vehiculo.lesiones_corporales == '25,000.00/50,000.00'):
            base_lesiones = 90
        elif (vehiculo.lesiones_corporales == '50,000.00/100,000.00'):
            base_lesiones = 120
        else:
            base_lesiones = 150

        if (vehiculo.danios_propiedad == '10,000.00'):
            base_danios = 120
        elif (vehiculo.danios_propiedad == '15,000.00'):
            base_danios = 140
        elif (vehiculo.danios_propiedad == '20,000.00'):
            base_danios = 150
        elif (vehiculo.danios_propiedad == '25,000.00'):
            base_danios = 160
        elif (vehiculo.danios_propiedad == '50,000.00'):
            base_danios = 170
        else:
            base_danios = 180

        if (vehiculo.gastos_medicos == '500.00/2,500.00'):
            base_gastos = 15
        elif (vehiculo.gastos_medicos == '1,000.00/5,000.00'):
            base_gastos = 25
        elif (vehiculo.gastos_medicos == '2,000.00/10,000.00'):
            base_gastos = 35
        elif (vehiculo.gastos_medicos == '5,000.00/25,000.00'):
            base_gastos = 50
        elif (vehiculo.gastos_medicos == '10,000.00/50,000.00'):
            base_gastos = 75
        else:
            base_gastos = 80

        prima_lesiones = float(
            "{0:.2f}".format((1 - descuento) * base_lesiones))
        prima_danios = float("{0:.2f}".format((1 - descuento) * base_danios))
        prima_gastos = float("{0:.2f}".format((1 - descuento) * base_gastos))

        if antig == 0:
            porcentaje_uso = 0.013
        elif antig == 1:
            porcentaje_uso = 0.013
        elif antig == 2:
            porcentaje_uso = 0.015
        elif antig == 3:
            porcentaje_uso = 0.017
        elif antig == 4:
            porcentaje_uso = 0.019
        elif antig == 5:
            porcentaje_uso = 0.022
        elif antig == 6:
            porcentaje_uso = 0.024
        elif antig == 7:
            porcentaje_uso = 0.027
        elif antig == 8:
            porcentaje_uso = 0.029
        else:
            porcentaje_uso = 0.033

        if antig == 0:
            base_colision = vehiculo.valor * 0.032
        elif antig == 1:
            base_colision = vehiculo.valor * 0.032
        elif antig == 2:
            base_colision = vehiculo.valor * 0.037
        elif antig == 3:
            base_colision = vehiculo.valor * 0.042
        elif antig == 4:
            base_colision = vehiculo.valor * 0.047
        elif antig == 5:
            base_colision = vehiculo.valor * 0.053
        elif antig == 6:
            base_colision = vehiculo.valor * 0.059
        elif antig == 7:
            base_colision = vehiculo.valor * 0.065
        elif antig == 8:
            base_colision = vehiculo.valor * 0.071
        else:
            base_colision = vehiculo.valor * 0.077

        deducibles = float(vehiculo.valor) * porcentaje_uso
        deducibles = float("{0:.2f}".format(deducibles))
        prima_otros = float(
            "{0:.2f}".format(deducibles - (deducibles * descuento)))
        prima_colision = float(
            "{0:.2f}".format(base_colision * (1 - descuento)))
        deducible_colision = base_colision * (1 + vehiculo.modelo.recargo)
        subtotal = prima_lesiones +\
            prima_danios + prima_gastos +\
            prima_otros + importacion_piezas + prima_colision + 75.00
        subtotal = float("{0:.2f}".format(subtotal))
        impuestos = float("{0:.2f}".format(subtotal * 0.06))
        total = float("{0:.2f}".format(subtotal + impuestos))
        prima_contado = float("{0:.2f}".format(total - (total * 0.10)))
        prima_ach = float("{0:.2f}".format(total - (total * 0.05)))

        user = User.objects.get(pk=request.user.id)
        if request.POST['endoso'] == "Basico":
            endoso = "Básico"
        else:
            endoso = request.POST['endoso']

        cotizacion = Cotizacion(
            conductor=conductor,
            corredor=user,
            lesiones_corporales=vehiculo.lesiones_corporales,
            danios_propiedad=vehiculo.danios_propiedad,
            gastos_medicos=vehiculo.gastos_medicos,
            otros_danios=deducibles,
            incendio_rayo=deducibles,
            robo_hurto=deducibles,
            importacion_piezas=importa,
            prima_lesiones=prima_lesiones,
            prima_daniosProp=prima_danios,
            prima_gastosMedicos=prima_gastos,
            prima_otrosDanios=prima_otros,
            subtotal=subtotal,
            prima_pagoContado=prima_contado,
            prima_pagoVisa=prima_ach,
            descuento=descuento,
            total=total,
            prima_colisionVuelco=prima_colision,
            colision_vuelco=deducible_colision,
            impuestos=impuestos,
            prima_importacion=importacion_piezas,
            plan="Básico",
            endoso=endoso)
        cotizacion.save()

        return cotizacion

    def post(self, request, *args, **kwargs):
        form = ConductorVehiculoForm(request.POST)
        if form.is_valid():
            if request.POST['endoso'] == "Basico":
                endoso = "Básico"
            else:
                endoso = request.POST['endoso']
            vehiculo = form.save()
            user = User.objects.get(pk=request.user.id)
            vehiculo.corredor = user
            vehiculo.save()
            cotizacion1 = self.crear_cotizacion(request, vehiculo)
            deducibles2 = float(
                "{0:.2f}".format(cotizacion1.otros_danios * 1.20))
            cotizacion2 = Cotizacion(
                conductor=vehiculo,
                corredor=user,
                lesiones_corporales=cotizacion1.lesiones_corporales,
                danios_propiedad=cotizacion1.danios_propiedad,
                gastos_medicos=cotizacion1.gastos_medicos,
                otros_danios=deducibles2,
                incendio_rayo=deducibles2,
                robo_hurto=deducibles2,
                importacion_piezas=cotizacion1.importacion_piezas,
                prima_lesiones=cotizacion1.prima_lesiones,
                prima_daniosProp=cotizacion1.prima_daniosProp,
                prima_gastosMedicos=cotizacion1.prima_gastosMedicos,
                prima_otrosDanios=cotizacion1.prima_otrosDanios * 0.9,
                prima_colisionVuelco=cotizacion1.prima_colisionVuelco * 0.9,
                colision_vuelco=cotizacion1.colision_vuelco * 1.20,
                descuento=cotizacion1.descuento,
                prima_importacion=cotizacion1.prima_importacion,
                plan="Premium",
                endoso=endoso)
            subtotal2 = cotizacion2.prima_lesiones +\
                cotizacion2.prima_daniosProp +\
                cotizacion2.prima_gastosMedicos +\
                cotizacion2.prima_otrosDanios +\
                cotizacion2.prima_importacion +\
                cotizacion2.prima_colisionVuelco + 75.00
            subtotal2 = float("{0:.2f}".format(subtotal2))
            impuestos2 = float("{0:.2f}".format(subtotal2 * 0.06))
            total2 = float("{0:.2f}".format(subtotal2 + impuestos2))
            prima_contado2 = float("{0:.2f}".format(total2 - (total2 * 0.10)))
            prima_ach2 = float("{0:.2f}".format(total2 - (total2 * 0.05)))
            cotizacion2.subtotal = subtotal2
            cotizacion2.prima_pagoContado = prima_contado2
            cotizacion2.prima_pagoVisa = prima_contado2
            cotizacion2.prima_pagoVisa = prima_ach2
            cotizacion2.total = total2
            cotizacion2.impuestos = impuestos2
            cotizacion2.save()

            ###################################
            deducibles3 = float(
                "{0:.2f}".format(cotizacion1.otros_danios * 1.60))

            cotizacion3 = Cotizacion(
                conductor=vehiculo,
                corredor=user,
                lesiones_corporales=cotizacion1.lesiones_corporales,
                danios_propiedad=cotizacion1.danios_propiedad,
                gastos_medicos=cotizacion1.gastos_medicos,
                otros_danios=deducibles3,
                incendio_rayo=deducibles3,
                robo_hurto=deducibles3,
                importacion_piezas=cotizacion1.importacion_piezas,
                prima_lesiones=cotizacion1.prima_lesiones,
                prima_daniosProp=cotizacion1.prima_daniosProp,
                prima_gastosMedicos=cotizacion1.prima_gastosMedicos,
                prima_otrosDanios=cotizacion1.prima_otrosDanios * 0.8,
                prima_colisionVuelco=cotizacion1.prima_colisionVuelco * 0.8,
                colision_vuelco=cotizacion1.colision_vuelco * 1.60,
                descuento=cotizacion1.descuento,
                prima_importacion=cotizacion1.prima_importacion,
                plan="Gold",
                endoso=endoso)
            subtotal3 = cotizacion3.prima_lesiones +\
                cotizacion3.prima_daniosProp +\
                cotizacion3.prima_gastosMedicos +\
                cotizacion3.prima_otrosDanios +\
                cotizacion3.prima_importacion +\
                cotizacion3.prima_colisionVuelco + 75.00
            subtotal3 = float("{0:.2f}".format(subtotal3))
            impuestos3 = float("{0:.2f}".format(subtotal3 * 0.06))
            total3 = float("{0:.2f}".format(subtotal3 + impuestos3))
            prima_contado3 = float("{0:.2f}".format(total3 - (total3 * 0.10)))
            prima_ach3 = float("{0:.2f}".format(total3 - (total3 * 0.05)))
            cotizacion3.subtotal = subtotal3
            cotizacion3.prima_pagoContado = prima_contado3
            cotizacion3.prima_pagoVisa = prima_contado3
            cotizacion3.prima_pagoVisa = prima_ach3
            cotizacion3.total = total3
            cotizacion3.impuestos = impuestos3
            cotizacion3.save()

            ###################################

            ###################################
            deducibles4 = float(
                "{0:.2f}".format(cotizacion1.otros_danios * 2.00))

            cotizacion4 = Cotizacion(
                conductor=vehiculo,
                corredor=user,
                lesiones_corporales=cotizacion1.lesiones_corporales,
                danios_propiedad=cotizacion1.danios_propiedad,
                gastos_medicos=cotizacion1.gastos_medicos,
                otros_danios=deducibles4,
                incendio_rayo=deducibles4,
                robo_hurto=deducibles4,
                importacion_piezas=cotizacion1.importacion_piezas,
                prima_lesiones=cotizacion1.prima_lesiones,
                prima_daniosProp=cotizacion1.prima_daniosProp,
                prima_gastosMedicos=cotizacion1.prima_gastosMedicos,
                prima_otrosDanios=cotizacion1.prima_otrosDanios * 0.7,
                prima_colisionVuelco=cotizacion1.prima_colisionVuelco * 0.7,
                colision_vuelco=cotizacion1.colision_vuelco * 2.00,
                descuento=cotizacion1.descuento,
                prima_importacion=cotizacion1.prima_importacion,
                plan="Silver",
                endoso=endoso)
            subtotal4 = cotizacion4.prima_lesiones +\
                cotizacion4.prima_daniosProp +\
                cotizacion4.prima_gastosMedicos +\
                cotizacion4.prima_otrosDanios +\
                cotizacion4.prima_importacion +\
                cotizacion4.prima_colisionVuelco + 75.00
            subtotal4 = float("{0:.2f}".format(subtotal4))
            impuestos4 = float("{0:.2f}".format(subtotal4 * 0.06))
            total4 = float("{0:.2f}".format(subtotal4 + impuestos4))
            prima_contado4 = float("{0:.2f}".format(total4 - (total4 * 0.10)))
            prima_ach4 = float("{0:.2f}".format(total4 - (total4 * 0.05)))
            cotizacion4.subtotal = subtotal4
            cotizacion4.prima_pagoContado = prima_contado4
            cotizacion4.prima_pagoVisa = prima_contado4
            cotizacion4.prima_pagoVisa = prima_ach4
            cotizacion4.total = total4
            cotizacion4.impuestos = impuestos4
            cotizacion4.save()

            ###################################

            return HttpResponseRedirect(
                reverse_lazy('ver_planes', kwargs={'pk': cotizacion1.pk,
                                                   'pk2': cotizacion2.pk,
                                                   'pk3': cotizacion3.pk,
                                                   'pk4': cotizacion4.pk}))
        else:
            return render(request, self.template_name, {'form': form})


class VerPlanes(LoginRequiredMixin, generic.TemplateView):
    template_name = "cotizar/opciones_cotizaciones.html"
    model = Cotizacion

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        cotizacion1 = Cotizacion.objects.get(pk=kwargs['pk'])
        cotizacion2 = Cotizacion.objects.get(pk=kwargs['pk2'])
        cotizacion3 = Cotizacion.objects.get(pk=kwargs['pk3'])
        cotizacion4 = Cotizacion.objects.get(pk=kwargs['pk4'])
        context['cotizaciones'] = [cotizacion1,
                                   cotizacion2,
                                   cotizacion3,
                                   cotizacion4]
        return self.render_to_response(context)


class DetalleCotizacion(LoginRequiredMixin, generic.UpdateView):
    template_name = "cotizar/detalle_cotizacion.html"
    model = Cotizacion

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        cotizacion = Cotizacion.objects.get(pk=kwargs['pk'])
        context['cotizacion'] = cotizacion
        context['form'] = CotizacionUpdateForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        cotizacion = Cotizacion.objects.get(pk=kwargs['pk'])
        cuotas = request.POST['cuotas']
        cotizacion.cuota = cuotas
        cotizacion.prima_mensual = float(
            "{0:.2f}".format(cotizacion.total / cuotas))
        cotizacion.save()
        subject = "Acerta Seguros - Cotización de Vehículo"
        to = [cotizacion.conductor.correo]
        to_corredor = [request.user.email]
        from_email = 'donotreply@cotizadoracerta.com'

        ctx = {
            'cotizacion': cotizacion,
        }

        # Correo Cliente
        message = get_template('cotizar/email.html').render(Context(ctx))
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

        # Correo Corredor
        message_corredor = get_template('cotizar/email_corredores.html').render(Context(ctx))
        msg = EmailMessage(subject, message_corredor, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

        # Correo Admin
        if request.user.groups.first().name != "super_admin":
            admin = User.objects.filter(groups__name__in=["super_admin"])
            admins = []
            for adm in admin:
                admins.append(adm.email)
            msg = EmailMessage(subject, message_corredor, to=admins, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()

        return HttpResponseRedirect(reverse_lazy('vehiculo'))


class listModelsAjax(LoginRequiredMixin, generic.ListView):
    model = Modelo
    context_object_name = 'modelos'

    def get_queryset(self, *args, **kwargs):
        marca = get_object_or_404(Marca, pk__iexact=self.kwargs['pk'])
        return Modelo.objects.filter(marca=marca)

    def get(self, request, *args, **kwargs):
        self.kwargs['pk'] = request.GET['id']
        listModels = self.get_queryset()
        models = []
        for model in listModels:
            models.append({
                'id': model.pk,
                'nombre': model.nombre,
            })
        data = json.dumps(models)
        return HttpResponse(data, content_type='application/json')
