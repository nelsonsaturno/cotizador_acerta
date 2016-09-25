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
from administrador.models import *
from darientSessions.models import *
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.views.defaults import page_not_found
from django.contrib.humanize.templatetags.humanize import *
import json
import re
import math
from xhtml2pdf import pisa
from easy_pdf.views import PDFTemplateView

# from django.template.loader import render_to_string
# from django.template import RequestContext
# import ho.pisa as pisa
import cStringIO as StringIO
# import cgi
import os


def CargarCarros(request):
    file = open("carros.txt")
    for line in file:
        nline = line.split()
        if nline[0] != "MODELO":
            n = len(nline)
            disc = int(nline[n - 1][0] + nline[n - 1][1]) * 0.01
            recharg = int(nline[n - 2][0] + nline[n - 2][1]) * 0.01
            brand = nline[n - 3]
            name = ""
            for i in range(n - 4, -1, -1):
                if name == "":
                    name = str(nline[i])
                else:
                    name = str(nline[i]) + " " + name
            result = Marca.objects.filter(nombre=brand)
            if not result:
                new_brand = Marca(nombre=brand)
                new_brand.save()
                if disc > 0.57:
                    new_model = Modelo(nombre=name,
                                       marca=new_brand,
                                       descuento=1.00,
                                       recargo=recharg)
                else:
                    new_model = Modelo(nombre=name,
                                       marca=new_brand,
                                       descuento=disc,
                                       recargo=recharg)
                new_model.save()
            else:
                if disc > 0.57:
                    new_model = Modelo(nombre=name,
                                       marca=result.first(),
                                       descuento=1.00,
                                       recargo=recharg)
                else:
                    new_model = Modelo(nombre=name,
                                       marca=result.first(),
                                       descuento=disc,
                                       recargo=recharg)
                new_model.save()
    return HttpResponseRedirect(
        reverse_lazy('login'))


class CotizarAhora(LoginRequiredMixin, generic.TemplateView):
    template_name = "cotizar/cotiza_ahora.html"


class Vehiculo(LoginRequiredMixin, generic.CreateView):
    template_name = "cotizar/vehiculo.html"
    form_class = ConductorVehiculoForm

    def get(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data(**kwargs)

        # Chequeamos si es corredor, y creamos los planes para mostrar
        # if (request.user.groups.first().name == "corredor"):
        #     corredor = DatosCorredor.objects.get(user=request.user)
        #     planes = corredor.planes
        #     crear_planes = re.findall('"([^"]*)"', planes)

        # # Chequeamos si es vendedor, y creamos los planes del corredor correspondiente para mostrar
        # elif (request.user.groups.first().name == "vendedor"):
        #     vendedor = CorredorVendedor.objects.get(vendedor=request.user)
        #     corredor = DatosCorredor.objects.get(user=vendedor.corredor)
        #     planes = corredor.planes
        #     crear_planes = re.findall('"([^"]*)"', planes)

        # else:
        #     corredor = None
        #     crear_planes = []

        context['form'] = ConductorVehiculoForm
        #context['planes'] = crear_planes 
        return self.render_to_response(context)

    def crear_cotizacion(self, request, vehiculo):
        conductor = vehiculo

        sexo = Sexo.objects.get(sexo=conductor.sexo)

        today = date.today()
        calc_edad = today.year - conductor.fecha_nacimiento.year - ((today.month, today.day) < (conductor.fecha_nacimiento.month, conductor.fecha_nacimiento.day))

        if calc_edad >= 30:
            estado_civil = Estado_Civil.objects.get(
                estado_civil='Casado(a)'
            )
        else:
            estado_civil = Estado_Civil.objects.get(
                estado_civil=conductor.estado_civil
            )

        valor = Valor.objects.filter(inferior__lte=vehiculo.valor,
                                     superior__gte=vehiculo.valor).first()

        if vehiculo.historial_transito == 0:
            historial_transito = Historial_Transito.objects.filter(
                inferior__lte=1,
                superior__gte=vehiculo.historial_transito
            ).first()
        else:
            historial_transito = Historial_Transito.objects.filter(
                inferior__lte=vehiculo.historial_transito,
                superior__gte=vehiculo.historial_transito
            ).first()

        # No kilometers.
        if vehiculo.cero_km or vehiculo.anio == date.today().year + 1:
            antig = 0
        else:
            antig = date.today().year - vehiculo.anio

        vejez = Antiguedad.objects.all().first()
        if antig <= vejez.limite:
            antiguedad = vejez.factor_menor
        else:
            antiguedad = vejez.factor_mayor

        edad = Edad.objects.filter(inferior__lte=calc_edad,
                                   superior__gte=calc_edad).first()

        desc_parametros = 1.00 -\
            (sexo.factor * estado_civil.factor * valor.factor *
             historial_transito.factor * antiguedad * edad.factor)

        descuento = min(vehiculo.modelo.descuento, desc_parametros)
        descuento = float("{0:.2f}".format(descuento))

        if descuento < 0.3:
            descuento = 0.3
        elif descuento > 0.625:
            descuento = 0.625

        factor_importacion = Importacion.objects.all().first()
        if vehiculo.importacion_piezas:
            importa = True
            importacion_piezas = float(
                "{0:.2f}".format(vehiculo.valor * factor_importacion.factor))
        else:
            importa = False
            importacion_piezas = 0.00

        base_lesiones = LesionesCorporales.objects.get(
            lesiones_corporales=vehiculo.lesiones_corporales
        )
        base_lesiones = base_lesiones.factor

        base_danios = DaniosPropiedad.objects.get(
            danios_propiedad=vehiculo.danios_propiedad
        )
        base_danios = base_danios.factor

        base_gastos = GastosMedicos.objects.get(
            gastos_medicos=vehiculo.gastos_medicos
        )
        base_gastos = base_gastos.factor

        prima_lesiones = float(
            "{0:.2f}".format((1 - descuento) * base_lesiones))
        prima_danios = float("{0:.2f}".format((1 - descuento) * base_danios))
        prima_gastos = float("{0:.2f}".format((1 - descuento) * base_gastos))

        if antig <= 1:
            porcentaje_uso = Tiempo_Uso.objects.get(tiempo=1)
        elif antig >= 9:
            porcentaje_uso = Tiempo_Uso.objects.get(tiempo=9)
        else:
            porcentaje_uso = Tiempo_Uso.objects.get(tiempo=antig)

        porcentaje_uso = porcentaje_uso.factor

        if antig <= 1:
            colision = Colision.objects.get(tiempo=1)
        elif antig >= 9:
            colision = Colision.objects.get(tiempo=9)
        else:
            colision = Colision.objects.get(tiempo=antig)

        base_colision = float("{0:.2f}".format(
            vehiculo.valor * colision.factor))

        endoso = Endoso.objects.get(pk=vehiculo.endoso.pk)
        prima_endoso = endoso.precio

        deducibles = float(vehiculo.valor) * porcentaje_uso
        deducibles = math.ceil(float("{0:.2f}".format(deducibles)))
        if deducibles < 150.00:
                deducibles = float("{0:.2f}".format(150.00))
        prima_otros = float(
            "{0:.2f}".format(deducibles - (deducibles * descuento)))
        prima_colision = float(
            "{0:.2f}".format(base_colision * (1 - descuento)))
        deducible_colision = math.ceil(float("{0:.0f}".format(int(
            base_colision * (1 + vehiculo.modelo.recargo)))))
        if deducible_colision < 250.00:
            deducible_colision = float("{0:.2f}".format(250.00))
        subtotal = prima_lesiones +\
            prima_danios + prima_gastos +\
            prima_otros + importacion_piezas + prima_colision + prima_endoso
        subtotal = float("{0:.2f}".format(subtotal))
        impuestos = float("{0:.2f}".format(subtotal * 0.06))
        total = float("{0:.2f}".format(subtotal + impuestos))
        prima_contado = float("{0:.2f}".format(total - (total * 0.10)))
        prima_ach = float("{0:.2f}".format(total - (total * 0.05)))

        user = User.objects.get(pk=request.user.id)

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
            endoso=endoso,
            prima_endoso=prima_endoso)
        cotizacion.save()

        return cotizacion

    def post(self, request, *args, **kwargs):
        form = ConductorVehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save()
            
            tipo_id = form.cleaned_data['tipo_id']
            if tipo_id == '0':
                provincia = form.cleaned_data['provincia']
                tipo = form.cleaned_data['tipo']
                campo_id_1 = form.cleaned_data['campo_id_1']
                campo_id_2 = form.cleaned_data['campo_id_2']
                cedula = str(provincia) + '-' + str(tipo) + '-' + str(campo_id_1) + '-' + str(campo_id_2)
                vehiculo.identificacion = cedula
                vehiculo.tipo_id = 'cedula'

            user = User.objects.get(pk=request.user.id)
            vehiculo.corredor = user
            vehiculo.save()
            cotizacion1 = self.crear_cotizacion(request, vehiculo)
            prima_endoso = cotizacion1.endoso.precio
            deducibles2 = math.ceil(float(
                "{0:.2f}".format(cotizacion1.otros_danios * 1.20)))
            if deducibles2 < 150.00:
                deducibles2 = float("{0:.2f}".format(150.00))
            colision_vuelco2 = float("{0:.0f}".format(
                    int(cotizacion1.colision_vuelco * 1.20)))
            if colision_vuelco2 < 250.00:
                colision_vuelco2 = float("{0:.2f}".format(250.00))
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
                colision_vuelco=math.ceil(colision_vuelco2),
                descuento=cotizacion1.descuento,
                prima_importacion=cotizacion1.prima_importacion,
                plan="Premium",
                endoso=cotizacion1.endoso,
                prima_endoso=prima_endoso)
            subtotal2 = cotizacion2.prima_lesiones +\
                cotizacion2.prima_daniosProp +\
                cotizacion2.prima_gastosMedicos +\
                cotizacion2.prima_otrosDanios +\
                cotizacion2.prima_importacion +\
                cotizacion2.prima_colisionVuelco + prima_endoso
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
            deducibles3 = math.ceil(float(
                "{0:.2f}".format(cotizacion1.otros_danios * 1.60)))
            if deducibles3 < 150.00:
                deducibles3 = float("{0:.2f}".format(150.00))
            colision_vuelco3 = float("{0:.0f}".format(
                    int(cotizacion1.colision_vuelco * 1.60)))
            if colision_vuelco3 < 250.00:
                colision_vuelco3 = float("{0:.2f}".format(250.00))

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
                colision_vuelco=math.ceil(colision_vuelco3),
                descuento=cotizacion1.descuento,
                prima_importacion=cotizacion1.prima_importacion,
                plan="Gold",
                endoso=cotizacion1.endoso,
                prima_endoso=prima_endoso)
            subtotal3 = cotizacion3.prima_lesiones +\
                cotizacion3.prima_daniosProp +\
                cotizacion3.prima_gastosMedicos +\
                cotizacion3.prima_otrosDanios +\
                cotizacion3.prima_importacion +\
                cotizacion3.prima_colisionVuelco + prima_endoso
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
            deducibles4 = math.ceil(float(
                "{0:.2f}".format(cotizacion1.otros_danios * 2.00)))
            if deducibles4 < 150.00:
                deducibles4 = float("{0:.2f}".format(150.00))
            colision_vuelco4 = float("{0:.0f}".format(
                    int(cotizacion1.colision_vuelco * 2.00)))
            if colision_vuelco4 < 250.00:
                colision_vuelco4 = float("{0:.2f}".format(250.00))

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
                colision_vuelco=math.ceil(colision_vuelco4),
                descuento=cotizacion1.descuento,
                prima_importacion=cotizacion1.prima_importacion,
                plan="Silver",
                endoso=cotizacion1.endoso,
                prima_endoso=prima_endoso)
            subtotal4 = cotizacion4.prima_lesiones +\
                cotizacion4.prima_daniosProp +\
                cotizacion4.prima_gastosMedicos +\
                cotizacion4.prima_otrosDanios +\
                cotizacion4.prima_importacion +\
                cotizacion4.prima_colisionVuelco + prima_endoso
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
            return render(request, self.template_name, {'form': form,
                                                        'update': True})


class VolverVehiculo(LoginRequiredMixin, generic.UpdateView):
    template_name = "cotizar/vehiculo.html"
    form_class = ConductorVehiculoForm
    model = ConductorVehiculo
    context_object_name = "vehiculo"

    def get_context_data(self, **kwargs):
        context = super(VolverVehiculo, self).get_context_data(**kwargs)
        context['update'] = True
        return context

    def crear_cotizacion(self, request, vehiculo):
        conductor = vehiculo

        sexo = Sexo.objects.get(sexo=conductor.sexo)
        today = date.today()
        calc_edad = today.year - conductor.fecha_nacimiento.year - ((today.month, today.day) < (conductor.fecha_nacimiento.month, conductor.fecha_nacimiento.day))

        if calc_edad >= 30:
            estado_civil = Estado_Civil.objects.get(
                estado_civil='Casado(a)'
            )
        else:
            estado_civil = Estado_Civil.objects.get(
                estado_civil=conductor.estado_civil
            )

        valor = Valor.objects.filter(inferior__lte=vehiculo.valor,
                                     superior__gte=vehiculo.valor).first()

        if vehiculo.historial_transito == 0:
            historial_transito = Historial_Transito.objects.filter(
                inferior__lte=1,
                superior__gte=vehiculo.historial_transito
            ).first()
        else:
            historial_transito = Historial_Transito.objects.filter(
                inferior__lte=vehiculo.historial_transito,
                superior__gte=vehiculo.historial_transito
            ).first()

        # No kilometers.
        if vehiculo.cero_km or vehiculo.anio == date.today().year + 1:
            antig = 0
        else:
            antig = date.today().year - vehiculo.anio

        vejez = Antiguedad.objects.all().first()
        if antig <= vejez.limite:
            antiguedad = vejez.factor_menor
        else:
            antiguedad = vejez.factor_mayor

        edad = Edad.objects.filter(inferior__lte=calc_edad,
                                   superior__gte=calc_edad).first()

        desc_parametros = 1.00 -\
            (sexo.factor * estado_civil.factor * valor.factor *
             historial_transito.factor * antiguedad * edad.factor)

        descuento = min(vehiculo.modelo.descuento, desc_parametros)
        descuento = float("{0:.2f}".format(descuento))

        if descuento < 0.3:
            descuento = 0.3
        elif descuento > 0.625:
            descuento = 0.625

        factor_importacion = Importacion.objects.all().first()
        if vehiculo.importacion_piezas:
            importa = True
            importacion_piezas = float(
                "{0:.2f}".format(vehiculo.valor * factor_importacion.factor))
        else:
            importa = False
            importacion_piezas = 0.00

        base_lesiones = LesionesCorporales.objects.get(
            lesiones_corporales=vehiculo.lesiones_corporales
        )
        base_lesiones = base_lesiones.factor

        base_danios = DaniosPropiedad.objects.get(
            danios_propiedad=vehiculo.danios_propiedad
        )
        base_danios = base_danios.factor

        base_gastos = GastosMedicos.objects.get(
            gastos_medicos=vehiculo.gastos_medicos
        )
        base_gastos = base_gastos.factor

        prima_lesiones = float(
            "{0:.2f}".format((1 - descuento) * base_lesiones))
        prima_danios = float("{0:.2f}".format((1 - descuento) * base_danios))
        prima_gastos = float("{0:.2f}".format((1 - descuento) * base_gastos))

        if antig <= 1:
            porcentaje_uso = Tiempo_Uso.objects.get(tiempo=1)
        elif antig >= 9:
            porcentaje_uso = Tiempo_Uso.objects.get(tiempo=9)
        else:
            porcentaje_uso = Tiempo_Uso.objects.get(tiempo=antig)

        porcentaje_uso = porcentaje_uso.factor

        if antig <= 1:
            colision = Colision.objects.get(tiempo=1)
        elif antig >= 9:
            colision = Colision.objects.get(tiempo=9)
        else:
            colision = Colision.objects.get(tiempo=antig)

        base_colision = float("{0:.2f}".format(
            vehiculo.valor * colision.factor))

        endoso = Endoso.objects.get(pk=vehiculo.endoso.pk)
        prima_endoso = endoso.precio

        deducibles = float(vehiculo.valor) * porcentaje_uso
        deducibles = float("{0:.2f}".format(deducibles))
        if deducibles < 150.00:
            deducibles = float("{0:.2f}".format(150.00))
        prima_otros = float(
            "{0:.2f}".format(deducibles - (deducibles * descuento)))
        prima_colision = float(
            "{0:.2f}".format(base_colision * (1 - descuento)))
        deducible_colision = float("{0:.0f}".format(
            int(base_colision * (1 + vehiculo.modelo.recargo))))
        if deducible_colision < 250.00:
            deducibles = float("{0:.2f}".format(250.00))
        subtotal = prima_lesiones +\
            prima_danios + prima_gastos +\
            prima_otros + importacion_piezas + prima_colision + prima_endoso
        subtotal = float("{0:.2f}".format(subtotal))
        impuestos = float("{0:.2f}".format(subtotal * 0.06))
        total = float("{0:.2f}".format(subtotal + impuestos))
        prima_contado = float("{0:.2f}".format(total - (total * 0.10)))
        prima_ach = float("{0:.2f}".format(total - (total * 0.05)))

        user = User.objects.get(pk=request.user.id)

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
            endoso=endoso,
            prima_endoso=prima_endoso)
        cotizacion.save()

        return cotizacion

    def post(self, request, *args, **kwargs):
        form = ConductorVehiculoForm(request.POST)
        if form.is_valid():
            self.object = form.save()
            vehiculo = self.object
            user = User.objects.get(pk=request.user.id)
            vehiculo.corredor = user
            vehiculo.save()
            cotizacion1 = self.crear_cotizacion(request, vehiculo)
            prima_endoso = cotizacion1.endoso.precio
            deducibles2 = float(
                "{0:.2f}".format(cotizacion1.otros_danios * 1.20))
            if deducibles2 < 150.00:
                deducibles2 = float("{0:.2f}".format(150.00))
            colision_vuelco2 = float("{0:.0f}".format(
                    int(cotizacion1.colision_vuelco * 1.20)))
            if colision_vuelco2 < 250.00:
                colision_vuelco2 = float("{0:.2f}".format(250.00))
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
                colision_vuelco=colision_vuelco2,
                descuento=cotizacion1.descuento,
                prima_importacion=cotizacion1.prima_importacion,
                plan="Premium",
                endoso=cotizacion1.endoso,
                prima_endoso=prima_endoso)
            subtotal2 = cotizacion2.prima_lesiones +\
                cotizacion2.prima_daniosProp +\
                cotizacion2.prima_gastosMedicos +\
                cotizacion2.prima_otrosDanios +\
                cotizacion2.prima_importacion +\
                cotizacion2.prima_colisionVuelco + prima_endoso
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
            if deducibles3 < 150.00:
                deducibles3 = float("{0:.2f}".format(150.00))
            colision_vuelco3 = float("{0:.0f}".format(
                    int(cotizacion1.colision_vuelco * 1.60)))
            if colision_vuelco3 < 250.00:
                colision_vuelco3 = float("{0:.2f}".format(250.00))

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
                colision_vuelco=colision_vuelco3,
                descuento=cotizacion1.descuento,
                prima_importacion=cotizacion1.prima_importacion,
                plan="Gold",
                endoso=cotizacion1.endoso,
                prima_endoso=prima_endoso)
            subtotal3 = cotizacion3.prima_lesiones +\
                cotizacion3.prima_daniosProp +\
                cotizacion3.prima_gastosMedicos +\
                cotizacion3.prima_otrosDanios +\
                cotizacion3.prima_importacion +\
                cotizacion3.prima_colisionVuelco + prima_endoso
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
            if deducibles4 < 150.00:
                deducibles4 = float("{0:.2f}".format(150.00))
            colision_vuelco4 = float("{0:.0f}".format(
                    int(cotizacion1.colision_vuelco * 2.00)))
            if colision_vuelco4 < 250.00:
                colision_vuelco4 = float("{0:.2f}".format(250.00))

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
                colision_vuelco=colision_vuelco4,
                descuento=cotizacion1.descuento,
                prima_importacion=cotizacion1.prima_importacion,
                plan="Silver",
                endoso=cotizacion1.endoso,
                prima_endoso=prima_endoso)
            subtotal4 = cotizacion4.prima_lesiones +\
                cotizacion4.prima_daniosProp +\
                cotizacion4.prima_gastosMedicos +\
                cotizacion4.prima_otrosDanios +\
                cotizacion4.prima_importacion +\
                cotizacion4.prima_colisionVuelco + prima_endoso
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
            if 'pkc' in kwargs:
                c_delete = Cotizacion.objects.get(pk=kwargs['pkc'])
                cotizacion1.version = c_delete.version + 1
                cotizacion2.version = c_delete.version + 1
                cotizacion3.version = c_delete.version + 1
                cotizacion4.version = c_delete.version + 1
                cotizacion1.save()
                cotizacion2.save()
                cotizacion3.save()
                cotizacion4.save()
                c_delete.delete()

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
        if cotizacion1.corredor.pk != request.user.pk:
            return page_not_found(request)
        elif cotizacion2.corredor.pk != request.user.pk:
            return page_not_found(request)
        elif cotizacion3.corredor.pk != request.user.pk:
            return page_not_found(request)
        elif cotizacion4.corredor.pk != request.user.pk:
            return page_not_found(request)
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
        if cotizacion.corredor.pk != request.user.pk:
            return page_not_found(request)
        context['cotizacion'] = cotizacion
        context['form'] = CotizacionUpdateForm()
        context['pk1'] = kwargs['pk1']
        context['pk2'] = kwargs['pk2']
        context['pk3'] = kwargs['pk3']
        context['pk4'] = kwargs['pk4']
        return self.render_to_response(context)

    def fetch_resources(self, uri, rel):
            path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

            return path    

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        cotizacion = Cotizacion.objects.get(pk=kwargs['pk'])
        cotizaciones = [kwargs['pk1'], kwargs['pk2'],
                            kwargs['pk3'], kwargs['pk4']]
        form = CotizacionUpdateForm(request.POST)
        cuotas = 1
        if form.is_valid():
            tipo_pago = int(request.POST['tipo_pago'])
            if tipo_pago == 0:
                cotizacion.cuota = 1
                cotizacion.tipo_pago = 'Contado'
            elif tipo_pago == 1:
                cuotas = request.POST['cuotas']
                cotizacion.tipo_pago = 'ACH'
                cotizacion.cuota = int(cuotas)
            elif tipo_pago == 2:
                cuotas = request.POST['cuotas3']
                cotizacion.tipo_pago = 'Visa'
                cotizacion.cuota = int(cuotas)
            else:
                cuotas = request.POST['cuotas2']
                cotizacion.tipo_pago = 'Otro'
                cotizacion.cuota = int(cuotas)
            if tipo_pago == 0:
                cotizacion.prima_mensual = float(
                "{0:.2f}".format(cotizacion.prima_pagoContado / float(cotizacion.cuota)))
            elif tipo_pago == 1:
                cotizacion.prima_mensual = float(
                "{0:.2f}".format(cotizacion.prima_pagoVisa / float(cotizacion.cuota)))
            elif tipo_pago == 2:
                cotizacion.prima_mensual = float(
                "{0:.2f}".format(cotizacion.prima_pagoVisa / float(cotizacion.cuota)))
            else:
                cotizacion.prima_mensual = float(
                "{0:.2f}".format(cotizacion.total / float(cotizacion.cuota)))
            cotizacion.is_active = True
            if request.POST['guardar'] == "guardalo":
                cotizacion.status = 'Guardada'
            else:
                cotizacion.status = 'Enviada'
            cotizacion.save()

            valor_vehiculo = intcomma(
                float("{0:.2f}".format(cotizacion.conductor.valor)))
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
                impuestos = impuestos + '0'
            if total[-2] == '.':
                total = total + '0'
            if prima_pagoVisa[-2] == '.':
                prima_pagoVisa = prima_pagoVisa + '0'
            if prima_contado[-2] == '.':
                prima_contado = prima_contado + '0'
            if prima_endoso[-2] == '.':
                prima_endoso = prima_endoso + '0'

            cot = []
            for cotiz in cotizaciones:
                cotizac = Cotizacion.objects.get(pk=cotiz)
                cot.append(cotizac)
            elegida = 1
            for cotiz in cotizaciones:
                if kwargs['pk'] > cotiz:
                    elegida += 1
            context = Context({'pagesize': 'letter',
                               'elegida': elegida,
                               'cotizacion': cotizacion,
                               'cotizaciones': cot,
                               'cotizacion1':cot[0],
                               'cotizacion2':cot[1],
                               'cotizacion3':cot[2],
                               'cotizacion4':cot[3],
                               'tipo_pago': cotizacion.tipo_pago,
                               'total': total,
                               'subtotal': subtotal,
                               'impuestos': impuestos,
                               'cuotas': cuotas})
            template = get_template('cotizar/opciones_cotizaciones_pdf.html')
            html = template.render(context)

            file = open("polizas/" + 'opciones.pdf', "w+b")

            context = Context({'pagesize': 'letter'})
            links = lambda uri, rel: os.path.join(settings.STATIC_ROOT2, uri.replace(settings.STATIC_URL, ""))
            pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=file, encoding='UTF-8', link_callback=links)

            file.seek(0)
            pdf = file.read()
            file.close()    

            for cotiz in cotizaciones:
                if cotiz != kwargs['pk']:
                    cotizac = Cotizacion.objects.get(pk=cotiz)
                    cotizac.delete()

            if request.POST['guardar'] == "guardalo":
                return HttpResponseRedirect(reverse_lazy('vehiculo'))
            else:
                subject = "Acerta Seguros - Cotización de Vehículo"
                to = [cotizacion.conductor.correo]
                to_corredor = [request.user.email]
                from_email = request.user.email

                valor_vehiculo = intcomma(
                    float("{0:.2f}".format(cotizacion.conductor.valor)))
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
                    impuestos = impuestos + '0'
                if total[-2] == '.':
                    total = total + '0'
                if prima_pagoVisa[-2] == '.':
                    prima_pagoVisa = prima_pagoVisa + '0'
                if prima_contado[-2] == '.':
                    prima_contado = prima_contado + '0'
                if prima_endoso[-2] == '.':
                    prima_endoso = prima_endoso + '0'

                opcion = 1
                if kwargs['pk'] > kwargs['pk1']:
                    opcion += 1
                if kwargs['pk'] > kwargs['pk2']:
                    opcion += 1
                if kwargs['pk'] > kwargs['pk3']:
                    opcion += 1
                if kwargs['pk'] > kwargs['pk4']:
                    opcion += 1

                ctx = {
                    'opcion': opcion,
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

                # Correo Cliente
                message = get_template('cotizar/email.html').render(Context(ctx))
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.attach("opciones.pdf",
                           pdf,
                           'application/pdf')
                msg.attach(cotizacion.endoso.archivo.name.split('/', 20)[-1],
                           open(cotizacion.endoso.archivo.name,
                                'rb').read(),
                           'application/pdf')
                
                msg.send()

                # Correo Corredor
                message_corredor = get_template('cotizar/email_corredores.html')\
                    .render(Context(ctx))
                msg = EmailMessage(subject,
                                   message_corredor,
                                   to=to_corredor)
                msg.content_subtype = 'html'
                msg.send()

                # Correo Admins
                admins = ['jgutierrez@acertaseguros.com', 'ylezcano@acertaseguros.com']
                msg = EmailMessage(subject,
                                   message_corredor,
                                   to=admins)
                msg.content_subtype = 'html'
                msg.send()

            #return HttpResponse(pdf, 'application/pdf')
            return HttpResponseRedirect(reverse_lazy('vehiculo'))
        else:
            context['cotizacion'] = cotizacion
            context['form'] = form
            context['pk1'] = kwargs['pk1']
            context['pk2'] = kwargs['pk2']
            context['pk3'] = kwargs['pk3']
            context['pk4'] = kwargs['pk4']
            return render(request, self.template_name, context)


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
