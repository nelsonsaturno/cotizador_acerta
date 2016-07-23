from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import *
from cotizador_acerta.views_mixins import *
from darientSessions.models import *
from cotizar.models import *
from django.contrib.auth.models import User
from django.views.defaults import page_not_found
from reportes.forms import *
import datetime
from time import *


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
        if cotizacion.corredor.pk != request.user.pk:
            return page_not_found(request)
        context['cotizacion'] = cotizacion
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
            vendedor = CorredorVendedor.objects.filter(corredor=user)
            if len(vendedor) == 0:
                return page_not_found(request)
            if vendedor[0].corredor.pk != request.user.pk:
                return page_not_found(request)
            vendedores = CorredorVendedor.objects.filter(corredor=user)
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
        elif request.user.groups.first().name == 'super_admin':
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
        return self.render_to_response(context)


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
        start = datetime.date.today() - timedelta(days=30)
        end = datetime.date.today()
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
            end = date.today()
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
        start = datetime.date.today() - timedelta(days=30)
        end = datetime.date.today()
        if request.user.groups.first().name == 'super_admin':
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
            end = date.today()
        if request.user.groups.first().name == 'super_admin':
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
