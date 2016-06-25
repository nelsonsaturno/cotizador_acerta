#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from cotizar.forms import *
from cotizador_acerta.views_mixins import LoginRequiredMixin
from cotizar.models import Conductor as ModeloConductor, Cotizacion


class CotizarAhora(LoginRequiredMixin, generic.TemplateView):
    template_name = "cotizar/cotiza_ahora.html"


class Conductor(LoginRequiredMixin, generic.CreateView):
    template_name = "cotizar/conductor.html"
    form_class = ConductorForm

    def post(self, request, *args, **kwargs):
        form = ConductorForm(request.POST)
        if form.is_valid():
            conductor = form.save()
            conductor
            return HttpResponseRedirect(reverse_lazy('vehiculo', kwargs={'pk': conductor.pk}))
        else:
            return render(request, self.template_name, {'form': form})


class Vehiculo(LoginRequiredMixin, generic.CreateView):
    template_name = "cotizar/vehiculo.html"
    form_class = VehiculoForm

    def crear_cotizacion(self, request, vehiculo):
        conductor = ModeloConductor.objects.get(pk=vehiculo.conductor.pk)
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
        elif (conductor.historial_transito >= 4) and (conductor.historial_transito <= 7):
            historial_transito = 1.10
        else:
            historial_transito = 1.20

        if vehiculo.antiguedad == 'Menor':
            antiguedad = 0.43
        else:
            antiguedad = 0.50

        if conductor.edad <= 25:
            edad = 1.10
        elif (conductor.edad >= 26) and (conductor.edad <= 65):
            edad = 0.98
        else:
            edad = 1.00

        desc_parametros = 1.00 - (sexo * estado_civil * valor * historial_transito * antiguedad * edad)

        descuento = min(vehiculo.modelo.descuento, desc_parametros)
        descuento = float("{0:.2f}".format(descuento))

        if descuento < 0.3:
            descuento = 0.3
        elif descuento > 0.625:
            descuento = 0.625

        lesiones_corporales = '25,000.00/50,000.00'
        danios_propiedad = '50,000.00'
        gastos_medicos = '2,000.00/10,000.00'
        if vehiculo.importacion_piezas:
            importa = True
            importacion_piezas = float("{0:.2f}".format(vehiculo.valor * 0.0018))
        else:
            importa = False
            importacion_piezas = 0.00

        prima_lesiones = float("{0:.2f}".format((1 - descuento) * 90.00))
        prima_danios = float("{0:.2f}".format((1 - descuento) * 170.00))
        prima_gastos = float("{0:.2f}".format((1 - descuento) * 35.00))

        if vehiculo.uso == 1:
            porcentaje_uso = 0.013
        elif vehiculo.uso == 2:
            porcentaje_uso = 0.015
        elif vehiculo.uso == 3:
            porcentaje_uso = 0.017
        elif vehiculo.uso == 4:
            porcentaje_uso = 0.019
        elif vehiculo.uso == 5:
            porcentaje_uso = 0.022
        elif vehiculo.uso == 6:
            porcentaje_uso = 0.024
        elif vehiculo.uso == 7:
            porcentaje_uso = 0.027
        elif vehiculo.uso == 8:
            porcentaje_uso = 0.029
        elif vehiculo.uso == 9:
            porcentaje_uso = 0.033

        deducibles = float(vehiculo.valor) * porcentaje_uso
        deducibles = float("{0:.2f}".format(deducibles))
        prima_otros = float("{0:.2f}".format(deducibles - (deducibles * descuento)))
        subtotal = prima_lesiones + prima_danios + prima_gastos + prima_otros + importacion_piezas + 75.00
        subtotal = float("{0:.2f}".format(subtotal))
        impuestos = float("{0:.2f}".format(subtotal * 0.06))
        total = float("{0:.2f}".format(subtotal + impuestos))
        prima_mensual = float("{0:.2f}".format(total * 0.10))
        prima_contado = float("{0:.2f}".format(total - (total * 0.10)))
        prima_ach = float("{0:.2f}".format(total - (total * 0.05)))

        user = User.objects.get(pk=request.user.id)

        cotizacion = Cotizacion(conductor=conductor,
        						vehiculo=vehiculo,
        						corredor=user,
        						lesiones_corporales=lesiones_corporales,
        						danios_propiedad=danios_propiedad,
        						gastos_medicos=gastos_medicos,
        						otros_danios=deducibles,
        						incendio_rayo=deducibles,
        						robo_hurto=deducibles,
        						importacion_piezas=importa,
        						prima_lesiones=prima_lesiones,
        						prima_daniosProp=prima_danios,
        						prima_gastosMedicos=prima_gastos,
        						prima_otrosDanios=prima_otros,
        						subtotal=subtotal,
        						prima_mensual=prima_mensual,
        						prima_pagoContado=prima_contado,
        						prima_pagoVisa=prima_ach,
        						descuento=descuento,
        						total=total,
        						impuestos=impuestos,
        						prima_importacion=importacion_piezas,
        						plan="Básico")
        cotizacion.save()

        return cotizacion

    def post(self, request, *args, **kwargs):
        form = VehiculoForm(request.POST)
        if form.is_valid():
            conductor = ModeloConductor.objects.get(pk=kwargs['pk'])
            vehiculo = form.save()
            vehiculo.conductor = conductor
            vehiculo.save()
            user = User.objects.get(pk=request.user.id)
            cotizacion1 = self.crear_cotizacion(request, vehiculo)
            deducibles2 = float("{0:.2f}".format(cotizacion1.otros_danios * 1.20))
            cotizacion2 = Cotizacion(conductor=conductor,
            						 vehiculo=vehiculo,
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
            						 descuento=cotizacion1.descuento,
            						 prima_importacion=cotizacion1.prima_importacion,
            						 plan="Premium")
            subtotal2 = cotizacion2.prima_lesiones + cotizacion2.prima_daniosProp + cotizacion2.prima_gastosMedicos + cotizacion2.prima_otrosDanios + cotizacion2.prima_importacion + 75.00
            subtotal2 = float("{0:.2f}".format(subtotal2))
            impuestos2 = float("{0:.2f}".format(subtotal2 * 0.06))
            total2 = float("{0:.2f}".format(subtotal2 + impuestos2))
            prima_mensual2 = float("{0:.2f}".format(total2 * 0.10))
            prima_contado2 = float("{0:.2f}".format(total2 - (total2 * 0.10)))
            prima_ach2 = float("{0:.2f}".format(total2 - (total2 * 0.05)))
            cotizacion2.subtotal = subtotal2
            cotizacion2.prima_mensual = prima_mensual2
            cotizacion2.prima_pagoContado = prima_contado2
            cotizacion2.prima_pagoVisa = prima_contado2
            cotizacion2.prima_pagoVisa = prima_ach2
            cotizacion2.total = total2
            cotizacion2.impuestos = impuestos2
            cotizacion2.save()

            ###################################
            deducibles3 = float("{0:.2f}".format(cotizacion1.otros_danios * 1.60))

            cotizacion3 = Cotizacion(conductor=conductor,
            						 vehiculo=vehiculo,
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
            						 descuento=cotizacion1.descuento,
            						 prima_importacion=cotizacion1.prima_importacion,
            						 plan="Gold")
            subtotal3 = cotizacion3.prima_lesiones + cotizacion3.prima_daniosProp + cotizacion3.prima_gastosMedicos + cotizacion3.prima_otrosDanios + cotizacion3.prima_importacion + 75.00
            subtotal3 = float("{0:.2f}".format(subtotal3))
            impuestos3 = float("{0:.2f}".format(subtotal3 * 0.06))
            total3 = float("{0:.2f}".format(subtotal3 + impuestos3))
            prima_mensual3 = float("{0:.2f}".format(total3 * 0.10))
            prima_contado3 = float("{0:.2f}".format(total3 - (total3 * 0.10)))
            prima_ach3 = float("{0:.2f}".format(total3 - (total3 * 0.05)))
            cotizacion3.subtotal = subtotal3
            cotizacion3.prima_mensual = prima_mensual3
            cotizacion3.prima_pagoContado = prima_contado3
            cotizacion3.prima_pagoVisa = prima_contado3
            cotizacion3.prima_pagoVisa = prima_ach3
            cotizacion3.total = total3
            cotizacion3.impuestos = impuestos3
            cotizacion3.save()

            ###################################

            ###################################
            deducibles4 = float("{0:.2f}".format(cotizacion1.otros_danios * 2.00))

            cotizacion4 = Cotizacion(conductor=conductor,
            						 vehiculo=vehiculo,
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
            						 descuento=cotizacion1.descuento,
            						 prima_importacion=cotizacion1.prima_importacion,
            						 plan="Silver")
            subtotal4 = cotizacion4.prima_lesiones + cotizacion4.prima_daniosProp + cotizacion4.prima_gastosMedicos + cotizacion4.prima_otrosDanios + cotizacion4.prima_importacion + 75.00
            subtotal4 = float("{0:.2f}".format(subtotal4))
            impuestos4 = float("{0:.2f}".format(subtotal4 * 0.06))
            total4 = float("{0:.2f}".format(subtotal4 + impuestos4))
            prima_mensual4 = float("{0:.2f}".format(total4 * 0.10))
            prima_contado4 = float("{0:.2f}".format(total4 - (total4 * 0.10)))
            prima_ach4 = float("{0:.2f}".format(total4 - (total4 * 0.05)))
            cotizacion4.subtotal = subtotal4
            cotizacion4.prima_mensual = prima_mensual4
            cotizacion4.prima_pagoContado = prima_contado4
            cotizacion4.prima_pagoVisa = prima_contado4
            cotizacion4.prima_pagoVisa = prima_ach4
            cotizacion4.total = total4
            cotizacion4.impuestos = impuestos4
            cotizacion4.save()

            ###################################

            return HttpResponseRedirect(reverse_lazy('ver_planes', kwargs={'pk': cotizacion1.pk,
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
        context['cotizaciones'] = [cotizacion1, cotizacion2, cotizacion3, cotizacion4]
        return self.render_to_response(context)


class DetalleCotizacion(LoginRequiredMixin, generic.DetailView):
    template_name = "cotizar/detalle_cotizacion.html"
    model = Cotizacion

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        cotizacion = Cotizacion.objects.get(pk=kwargs['pk'])
        context['cotizacion'] = cotizacion
        return self.render_to_response(context)
