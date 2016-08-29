from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import *
from cotizador_acerta.views_mixins import *
from darientSessions.models import *
from cotizar.models import *
from django.contrib.auth.models import User
from django.views.defaults import page_not_found
from reportes.forms import *
import datetime
from datetime import *
from time import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.contrib.humanize.templatetags.humanize import *
from weasyprint import HTML


class CorredorVendedorListView(LoginRequiredMixin,
                               GroupRequiredMixin, ListView):
    model = DatosCorredor
    template_name = 'reportes/corredor_vendedor_list.html'

    def get_context_data(self, **kwargs):
        context = super(
            CorredorVendedorListView, self).get_context_data(**kwargs)
        vendedores = CorredorVendedor.objects.all()
        context['vendedores'] = vendedores
        return context


class CorredorVendedorDetailView(LoginRequiredMixin,
                                 DetailRequiredMixin, TemplateView):
    template_name = 'reportes/corredor_detail.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        if request.user.groups.first().name == 'corredor':
            vendedor = CorredorVendedor.objects.filter(vendedor=user)
            if len(vendedor) == 0:
                return page_not_found(request)
            if vendedor[0].corredor.pk != request.user.pk:
                return page_not_found(request)
        context = self.get_context_data(**kwargs)
        context['usuario'] = user
        if user.groups.first().name == 'corredor':
            context['corredor'] = DatosCorredor.objects.get(user=user)
        cotizaciones = Cotizacion.objects.filter(corredor=user, is_active=True)
        num_cot = len(cotizaciones)
        context['cotizaciones'] = cotizaciones
        context['num_cot'] = num_cot
        return self.render_to_response(context)


class VendedorListView(LoginRequiredMixin, CorredorRequiredMixin, ListView):
    template_name = 'reportes/vendedor_list.html'
    model = User

    def get(self, request, *args, **kwargs):
        self.object_list = []
        context = super(
            VendedorListView, self).get_context_data(**kwargs)
        corredor = User.objects.get(pk=request.user.pk)
        vendedores = CorredorVendedor.objects.filter(corredor=corredor)
        context['vendedores'] = vendedores
        return self.render_to_response(context)


class CotizacionesListView(LoginRequiredMixin, ListView):
    template_name = 'reportes/cotizaciones_list.html'
    model = Cotizacion

    def get(self, request, *args, **kwargs):
        self.object_list = []
        context = super(
            CotizacionesListView, self).get_context_data(**kwargs)
        corredor = User.objects.get(pk=request.user.pk)
        cotizaciones = Cotizacion.objects.filter(corredor=corredor, is_active=True)
        context['cotizaciones'] = cotizaciones
        return self.render_to_response(context)


class CotizacionesDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/cotizacion_details.html'
    model = Cotizacion

    def get(self, request, *args, **kwargs):
        context = super(
            CotizacionesDetailView, self).get_context_data(**kwargs)
        cotizacion = Cotizacion.objects.get(pk=kwargs['pk'], is_active=True)
        user = User.objects.get(pk=request.user.pk)
        all_admins = [
            'super_admin',
            'admin'
        ]
        groups = user.groups.filter(name__in=all_admins)

        if cotizacion.corredor.groups.first().name == "vendedor":
            my_user = User.objects.get(pk=cotizacion.corredor.pk)
            corredor = CorredorVendedor.objects.get(vendedor=my_user)

        if not groups:
            if cotizacion.corredor.pk != user.pk or corredor.corredor.pk != user.pk:
                return page_not_found(request)
        context['cotizacion'] = cotizacion
        context['active_user'] = user
        return self.render_to_response(context)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/dashboard.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        context = self.get_context_data(**kwargs)
        corredorCot = []
        vendedorCot = []
        # (Cotizaciones, Enviadas, Guardadas, Aprobadas, Rechazadas)
        numCot = [0, 0, 0, 0, 0]
        # Corredor view.
        if request.user.groups.first().name == 'corredor':
            vendedores = CorredorVendedor.objects.filter(corredor=user)
            for vend in vendedores:
                if vend.corredor.pk != request.user.pk:
                    return page_not_found(request)
            # Find out the seller's cotizations
            for vendedor in vendedores:
                cotizaciones = Cotizacion.objects.filter(
                    corredor=vendedor.vendedor, is_active=True)
                numCot[0] += len(cotizaciones)
                cotizaciones1 = cotizaciones.filter(status='Enviada')
                numCot[1] += len(cotizaciones1)
                cotizaciones2 = cotizaciones.filter(status='Guardada')
                numCot[2] += len(cotizaciones2)
                cotizaciones3 = cotizaciones.filter(status='Aprobada')
                numCot[3] += len(cotizaciones3)
                cotizaciones4 = cotizaciones.filter(status='Rechazada')
                numCot[4] += len(cotizaciones4)
                vendedorCot.append([vendedor,
                                    len(cotizaciones),
                                    len(cotizaciones1),
                                    len(cotizaciones2),
                                    len(cotizaciones3),
                                    len(cotizaciones4)])
            context['vendedores'] = vendedorCot
        # Admin view
        elif request.user.groups.first().name == 'super_admin'\
             or request.user.groups.first().name == "admin":
            corredores = DatosCorredor.objects.all()
            for corredor in corredores:
                cotizaciones = Cotizacion.objects.filter(
                    corredor=corredor.user, is_active=True)
                numCot[0] += len(cotizaciones)
                cotizaciones1 = cotizaciones.filter(status='Enviada')
                numCot[1] += len(cotizaciones1)
                cotizaciones2 = cotizaciones.filter(status='Guardada')
                numCot[2] += len(cotizaciones2)
                cotizaciones3 = cotizaciones.filter(status='Aprobada')
                numCot[3] += len(cotizaciones3)
                cotizaciones4 = cotizaciones.filter(status='Rechazada')
                numCot[4] += len(cotizaciones4)
                corredorCot.append([corredor,
                                    len(cotizaciones),
                                    len(cotizaciones1),
                                    len(cotizaciones2),
                                    len(cotizaciones3),
                                    len(cotizaciones4)])
            context['corredores'] = corredorCot
        #Session User.
        context['usuario'] = user
        if user.groups.first().name == 'corredor':
            context['corredor'] = DatosCorredor.objects.get(user=user)
        cotizaciones = Cotizacion.objects.filter(corredor=user, is_active=True)
        enviadas = Cotizacion.objects.filter(corredor=user, is_active=True, status='Enviada')
        guardadas = Cotizacion.objects.filter(corredor=user, is_active=True, status='Guardada')
        aceptadas = Cotizacion.objects.filter(corredor=user, is_active=True, status='Aprobada')
        rechazadas = Cotizacion.objects.filter(corredor=user, is_active=True, status='Rechazada')
        num_cot = len(cotizaciones) + numCot[0]
        context['cotizaciones'] = cotizaciones
        context['cot'] = len(cotizaciones)
        context['cot_env'] = len(enviadas)
        context['cot_guard'] = len(guardadas)
        context['cot_apr'] = len(aceptadas)
        context['cot_rch'] = len(rechazadas)
        context['num_cot'] = num_cot
        context['num_cot_env'] = len(enviadas) + numCot[1]
        context['num_cot_guard'] = len(guardadas) + numCot[2]
        context['num_cot_apr'] = len(aceptadas) + numCot[3]
        context['num_cot_rch'] = len(rechazadas) + numCot[4]
        form = DateCotizationForm()
        context['form'] = form
        start = datetime.strptime('1900-01-01', '%Y-%m-%d')
        end = datetime.strptime('1900-01-01', '%Y-%m-%d')
        context['start'] = start.strftime("%Y-%m-%d")
        context['end'] = end.strftime("%Y-%m-%d")
        context['date'] = '0'
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        context = self.get_context_data(**kwargs)
        form = DateCotizationForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
        else:
            start = date.today() - timedelta(days=30)
            end = date.today() + timedelta(days=1)
        corredorCot = []
        vendedorCot = []
        # (Cotizaciones, Enviadas, Guardadas, Aprobadas, Rechazadas)
        numCot = [0, 0, 0, 0, 0]
        # Corredor view.
        if request.user.groups.first().name == 'corredor':
            vendedores = CorredorVendedor.objects.filter(corredor=user)
            for vend in vendedores:
                if vend.corredor.pk != request.user.pk:
                    return page_not_found(request)
            # Find out the seller's cotizations
            for vendedor in vendedores:
                cotizaciones = Cotizacion.objects.filter(
                    corredor=vendedor.vendedor, is_active=True, created_at__lte=end,
                    created_at__gte=start)
                numCot[0] += len(cotizaciones)
                cotizaciones1 = cotizaciones.filter(status='Enviada')
                numCot[1] += len(cotizaciones1)
                cotizaciones2 = cotizaciones.filter(status='Guardada')
                numCot[2] += len(cotizaciones2)
                cotizaciones3 = cotizaciones.filter(status='Aprobada')
                numCot[3] += len(cotizaciones3)
                cotizaciones4 = cotizaciones.filter(status='Rechazada')
                numCot[4] += len(cotizaciones4)
                vendedorCot.append([vendedor,
                                    len(cotizaciones),
                                    len(cotizaciones1),
                                    len(cotizaciones2),
                                    len(cotizaciones3),
                                    len(cotizaciones4)])
            context['vendedores'] = vendedorCot
        # Admin view
        elif request.user.groups.first().name == 'super_admin'\
             or request.user.groups.first().name == "admin":
            corredores = DatosCorredor.objects.all()
            for corredor in corredores:
                cotizaciones = Cotizacion.objects.filter(
                    corredor=corredor.user, is_active=True, created_at__lte=end,
                    created_at__gte=start)
                numCot[0] += len(cotizaciones)
                cotizaciones1 = cotizaciones.filter(status='Enviada')
                numCot[1] += len(cotizaciones1)
                cotizaciones2 = cotizaciones.filter(status='Guardada')
                numCot[2] += len(cotizaciones2)
                cotizaciones3 = cotizaciones.filter(status='Aprobada')
                numCot[3] += len(cotizaciones3)
                cotizaciones4 = cotizaciones.filter(status='Rechazada')
                numCot[4] += len(cotizaciones4)
                corredorCot.append([corredor,
                                    len(cotizaciones),
                                    len(cotizaciones1),
                                    len(cotizaciones2),
                                    len(cotizaciones3),
                                    len(cotizaciones4)])
            context['corredores'] = corredorCot
        #Session User.
        context['usuario'] = user
        if user.groups.first().name == 'corredor':
            context['corredor'] = DatosCorredor.objects.get(user=user)
        cotizaciones = Cotizacion.objects.filter(corredor=user, is_active=True,created_at__lte=end,
                    created_at__gte=start)
        enviadas = Cotizacion.objects.filter(corredor=user, is_active=True, status='Enviada', created_at__lte=end,
                    created_at__gte=start)
        guardadas = Cotizacion.objects.filter(corredor=user, is_active=True, status='Guardada', created_at__lte=end,
                    created_at__gte=start)
        aceptadas = Cotizacion.objects.filter(corredor=user, is_active=True, status='Aprobada', created_at__lte=end,
                    created_at__gte=start)
        rechazadas = Cotizacion.objects.filter(corredor=user, is_active=True, status='Rechazada', created_at__lte=end,
                    created_at__gte=start)
        num_cot = len(cotizaciones) + numCot[0]
        context['cotizaciones'] = cotizaciones
        context['cot'] = len(cotizaciones)
        context['cot_env'] = len(enviadas)
        context['cot_guard'] = len(guardadas)
        context['cot_apr'] = len(aceptadas)
        context['cot_rch'] = len(rechazadas)
        context['num_cot'] = num_cot
        context['num_cot_env'] = len(enviadas) + numCot[1]
        context['num_cot_guard'] = len(guardadas) + numCot[2]
        context['num_cot_apr'] = len(aceptadas) + numCot[3]
        context['num_cot_rch'] = len(rechazadas) + numCot[4]
        context['form'] = form
        context['start'] = start.strftime("%Y-%m-%d")
        context['end'] = end.strftime("%Y-%m-%d")
        context['date'] = '1'
        return render(request, self.template_name, context)

class CotizacionesSpecificDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/cotizador_specific_detail.html'
    form_class = DateCotizationForm

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        context = self.get_context_data(**kwargs)
        if kwargs['status'] == '0':
            status = 'Enviada'
        elif kwargs['status'] == '1':
            status = 'Guardada'
        elif kwargs['status'] == '2':
            status = 'Aprobada'
        elif kwargs['status'] == '3':
            status = 'Rechazada'
        else:
            status = 'all'
        if int(kwargs['date']) == 0:
            start = date.today() - timedelta(days=5000)
            end = date.today() + timedelta(days=1)
        else:
            start = datetime.strptime(kwargs['start'], '%Y-%m-%d')
            end = datetime.strptime(kwargs['end'], '%Y-%m-%d')
        if status == 'all':
            cotizaciones = Cotizacion.objects.filter(
            corredor=user,
            is_active=True, created_at__lte=end,
            created_at__gte=start)
        else:
            cotizaciones = Cotizacion.objects.filter(
            corredor=user, status=status,
            is_active=True, created_at__lte=end,
            created_at__gte=start)
        if int(kwargs['pk']) == int(request.user.pk):
            context['propia'] = 'si'
        else:
            context['propia'] = 'no'
        context['cotizaciones'] = cotizaciones
        context['status'] = status
        context['form'] = DateCotizationForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        context = self.get_context_data(**kwargs)
        form = DateCotizationForm(request.POST)
        if kwargs['status'] == '0':
            status = 'Enviada'
        elif kwargs['status'] == '1':
            status = 'Guardada'
        elif kwargs['status'] == '2':
            status = 'Aprobada'
        elif kwargs['status'] == '3':
            status = 'Rechazada'
        else:
            status = 'all'
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
        else:
            start = date.today() - timedelta(days=30)
            end = date.today() + timedelta(days=1)
        if status == 'all':
            cotizaciones = Cotizacion.objects.filter(
            corredor=user,
            is_active=True, created_at__lte=end,
            created_at__gte=start)
        else:
            cotizaciones = Cotizacion.objects.filter(
            corredor=user, status=status,
            is_active=True, created_at__lte=end,
            created_at__gte=start)
        if int(kwargs['pk']) == int(request.user.pk):
            context['propia'] = 'si'
        else:
            context['propia'] = 'no'
        context['cotizaciones'] = cotizaciones
        context['status'] = status
        context['form'] = form
        if request.POST['start_date'] == '':
            form.add_error(
                None, "El campo de fecha de inicio es requerido.")
        if request.POST['end_date'] == '':
            form.add_error(
                None, "El campo de fecha final es requerido.")
        return render(request, self.template_name, context)


class CotizacionesGeneralDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/cotizador_general_detail.html'
    form_class = DateCotizationForm

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        context = self.get_context_data(**kwargs)
        cotizaciones = []
        if kwargs['status'] == '0':
            status = 'Enviada'
        elif kwargs['status'] == '1':
            status = 'Guardada'
        elif kwargs['status'] == '2':
            status = 'Aprobada'
        elif kwargs['status'] == '3':
            status = 'Rechazada'
        else:
            status = 'all'
        if int(kwargs['date']) == 0:
            start = date.today() - timedelta(days=5000)
            end = date.today() + timedelta(days=1)
        else:
            start = datetime.strptime(kwargs['start'], '%Y-%m-%d')
            end = datetime.strptime(kwargs['end'], '%Y-%m-%d')
        if request.user.groups.first().name == 'super_admin'\
           or request.user.groups.first().name == "admin":
            corredores = DatosCorredor.objects.all()
            for corredor in corredores:
                if status == 'all':
                    cotizaciones += Cotizacion.objects.filter(
                    corredor=corredor.user,
                    is_active=True, created_at__lte=end,
                    created_at__gte=start)
                else:
                    cotizaciones += Cotizacion.objects.filter(
                    corredor=corredor.user, status=status,
                    is_active=True, created_at__lte=end,
                    created_at__gte=start)
        elif request.user.groups.first().name == 'corredor':
            vendedores = CorredorVendedor.objects.filter(corredor=user)
            for vendedor in vendedores:
                if status == 'all':
                    cotizaciones += Cotizacion.objects.filter(
                    corredor=vendedor.vendedor,
                    is_active=True, created_at__lte=end,
                    created_at__gte=start)
                else:
                    cotizaciones += Cotizacion.objects.filter(
                    corredor=vendedor.vendedor, status=status,
                    is_active=True, created_at__lte=end,
                    created_at__gte=start)
        if status == 'all':
            cotizaciones += Cotizacion.objects.filter(
            corredor=user,
            is_active=True, created_at__lte=end,
            created_at__gte=start)
        else:
            cotizaciones += Cotizacion.objects.filter(
            corredor=user, status=status,
            is_active=True, created_at__lte=end,
            created_at__gte=start)
        context['cotizaciones'] = cotizaciones
        context['status'] = status
        context['form'] = DateCotizationForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        context = self.get_context_data(**kwargs)
        cotizaciones = []
        form = DateCotizationForm(request.POST)
        if kwargs['status'] == '0':
            status = 'Enviada'
        elif kwargs['status'] == '1':
            status = 'Guardada'
        elif kwargs['status'] == '2':
            status = 'Aprobada'
        elif kwargs['status'] == '3':
            status = 'Rechazada'
        else:
            status = 'all'
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
        else:
            start = date.today() - timedelta(days=30)
            end = date.today() + timedelta(days=1)
        if request.user.groups.first().name == 'super_admin'\
           or request.user.groups.first().name == "admin":
            corredores = DatosCorredor.objects.all()
            for corredor in corredores:
                if status == 'all':
                    cotizaciones += Cotizacion.objects.filter(
                    corredor=corredor.user,
                    is_active=True, created_at__lte=end,
                    created_at__gte=start)
                else:
                    cotizaciones += Cotizacion.objects.filter(
                    corredor=corredor.user, status=status,
                    is_active=True, created_at__lte=end,
                    created_at__gte=start)
        elif request.user.groups.first().name == 'corredor':
            vendedores = CorredorVendedor.objects.filter(corredor=user)
            for vendedor in vendedores:
                if status == 'all':
                    cotizaciones += Cotizacion.objects.filter(
                    corredor=vendedor.vendedor,
                    is_active=True, created_at__lte=end,
                    created_at__gte=start)
                else:
                    cotizaciones += Cotizacion.objects.filter(
                    corredor=vendedor.vendedor, status=status,
                    is_active=True, created_at__lte=end,
                    created_at__gte=start)
        if status == 'all':
            cotizaciones += Cotizacion.objects.filter(
            corredor=user,
            is_active=True, created_at__lte=end,
            created_at__gte=start)
        else:
            cotizaciones += Cotizacion.objects.filter(
            corredor=user, status=status,
            is_active=True, created_at__lte=end,
            created_at__gte=start)
        context['cotizaciones'] = cotizaciones
        context['status'] = status
        context['form'] = form
        if request.POST['start_date'] == '':
            form.add_error(
                None, "El campo de fecha de inicio es requerido.")
        if request.POST['end_date'] == '':
            form.add_error(
                None, "El campo de fecha final es requerido.")
        return render(request, self.template_name, context)


def changeStatus(request, id, status):
    cotizacion = Cotizacion.objects.get(pk=id)
    if int(status) == 0:
        cotizacion.status = "Aprobada"
        cotizacion.save()
        subject = "Acerta Seguros - Aprobada la Cotizacion de Vehiculo"

        admin = User.objects.filter(groups__name__in=["super_admin", "admin"])
        to = []
        for adm in admin:
            to.append(adm.email)
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
            impuestos = impuestos + '0'
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

        # Correo Cliente
        message = get_template('cotizar/email_corredores.html').render(Context(ctx))
        msg = EmailMessage(subject, message, to=to, from_email=from_email, cc=['nc@darient.com'])
        msg.content_subtype = 'html'
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
        admins = ['jgutierrez@acertaseguros.com', 'ylezcano@acertaseguros.com']
        msg = EmailMessage(subject,
                           message_corredor,
                           to=admins)
        msg.content_subtype = 'html'
        msg.send()
    else:
        cotizacion.status = "Rechazada"
        cotizacion.save()
    return HttpResponseRedirect(reverse_lazy('cotizaciones_list'))


def sendCotization(request, id):
    cotizacion = Cotizacion.objects.get(pk=id)
    if (cotizacion.status != 'Aprobada') and (cotizacion.status != 'Rechazada'):
        cotizacion.status = 'Enviada'
        cotizacion.save()
    subject = "Acerta Seguros - Cotizacion de Vehiculo"
    to = [cotizacion.conductor.correo]
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
        impuestos = impuestos + '0'
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

    # Correo Cliente
    message = get_template('cotizar/email.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
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

    return HttpResponseRedirect(reverse_lazy('cotizaciones_list'))


class ReportError(LoginRequiredMixin, FormView):
    form_class = ReportErrorForm
    template_name = 'reportes/reporte_error.html'

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        if form.is_valid():
            imagen = request.FILES['imagen']
            ctx = {
                'email': request.user.email,
                'nombre': request.user.first_name,
                'apellido': request.user.last_name,
                'descripcion': form.cleaned_data['descripcion']
            }
            subject = "Acerta Seguros - Reporte de Errores"
            to = ['ns@darient.com', 'nc@darient.com', 'og@darient.com']
            message = get_template(
                'reportes/html_reporte_email.html').render(Context(ctx))
            msg = EmailMessage(subject, message, to=to)
            msg.content_subtype = 'html'
            msg.attach(imagen.name, imagen.read(), imagen.content_type)
            msg.send()
            return HttpResponseRedirect(reverse_lazy('report_success'))
        else:
            return self.form_invalid(form)


class ReportSuccess(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/reporte_success.html'


class ShowPdf(TemplateView):
    template_name = 'reportes/mypdf.html'
