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
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context


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


def changeStatus(request, id, status):
    cotizacion = Cotizacion.objects.get(pk=id)
    if int(status) == 0:
        cotizacion.status = "Aprobada"
    else:
        cotizacion.status = "Rechazada"
    cotizacion.save()
    return HttpResponseRedirect(reverse_lazy('cotizaciones_list'))


def sendCotization(request, id):
    cotizacion = Cotizacion.objects.get(pk=id)
    cotizacion.status = 'Enviada'
    cotizacion.save()
    subject = "Acerta Seguros - Cotizacion de Vehiculo"
    to = [cotizacion.conductor.correo]
    to_corredor = [request.user.email]
    from_email = request.user.email

    ctx = {
        'cotizacion': cotizacion,
    }

    # Correo Cliente
    message = get_template('cotizar/email.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    if cotizacion.endoso == "Ford":
        msg.attach('ford.pdf',
                   open('cotizador_acerta/static/pdf/ford.pdf',
                        'rb').read(),
                   'application/pdf')

    if cotizacion.endoso == "Toyota":
        msg.attach('toyota.pdf',
                   open('cotizador_acerta/static/pdf/toyota.pdf',
                        'rb').read(),
                   'application/pdf')

    if cotizacion.endoso == "Lexus":
        msg.attach('lexus.pdf',
                   open('cotizador_acerta/static/pdf/lexus.pdf',
                        'rb').read(),
                   'application/pdf')

    if cotizacion.endoso == "Subaru":
        msg.attach('subaru.pdf',
                   open('cotizador_acerta/static/pdf/subaru.pdf',
                        'rb').read(),
                   'application/pdf')
    if cotizacion.endoso == "Porsche":
        msg.attach('porsche.pdf',
                   open('cotizador_acerta/static/pdf/porsche.pdf',
                        'rb').read(),
                   'application/pdf')
    if cotizacion.endoso == "Volvo":
        msg.attach('volvo.pdf',
                   open('cotizador_acerta/static/pdf/volvo.pdf',
                        'rb').read(),
                   'application/pdf')
    msg.send()

    # Correo Corredor
    message_corredor = get_template('cotizar/email_corredores.html')\
        .render(Context(ctx))
    msg = EmailMessage(subject,
                       message_corredor,
                       to=to_corredor,
                       from_email='noreply@acertaseguros.com')
    msg.content_subtype = 'html'
    msg.send()

    # Correo Admin
    if request.user.groups.first().name != "super_admin":
        admin = User.objects.filter(groups__name__in=["super_admin"])
        admins = []
        for adm in admin:
            admins.append(adm.email)
        msg = EmailMessage(subject,
                           message_corredor,
                           to=admins,
                           from_email='noreply@acertaseguros.com')
        msg.content_subtype = 'html'
        msg.send()

    return HttpResponseRedirect(reverse_lazy('cotizaciones_list'))
