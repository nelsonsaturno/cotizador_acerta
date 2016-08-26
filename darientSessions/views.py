#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import datetime
import random
import os
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import *
from django.core.urlresolvers import reverse_lazy
from django.core.mail import EmailMessage
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.views import generic
from cotizador_acerta.views_mixins import *
from darientSessions.models import *
from darientSessions.forms import *
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect
from darientSessions.forms import PasswordResetForm
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse
from django.views.defaults import page_not_found


def user_registration(request):
    if request.user.is_authenticated():
        # We obtain the user group by the user logged.
        # Sellers will created by agents
        # Agents will created by admins
        if (request.user.groups.first().name == "corredor")\
           or (request.user.groups.first().name == "super_admin")\
           or (request.user.groups.first().name == "admin"):
            if request.method == 'POST':
                if request.user.groups.first().name == "corredor":
                    form = UserCreateForm(request.POST)
                else:
                    form = CorredorCreateForm(request.POST)

                if form.is_valid():
                    my_user = form.save()
                    username = my_user.username
                    email = form.cleaned_data['email']
                    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                    activation_key = hashlib.sha1(salt + email).hexdigest()
                    key_expires = datetime.datetime.today() +\
                        datetime.timedelta(2)
                    user = User.objects.get(username=username)
                    new_profile = UserProfile(user=user,
                                              activation_key=activation_key,
                                              key_expires=key_expires)
                    new_profile.save()

                    email_subject = 'Bienvenido(a) a Acerta Seguros'
                    to = [email]
                    link = 'http://' + request.get_host() + '/accounts/confirm/' + activation_key + '/' + str(user.pk)
                    if user.first_name and user.last_name:
                        iniciales = user.first_name[0] + user.last_name[0]
                    else:
                        iniciales = user.username[:2]
                    ctx = {
                        'user': user,
                        'link': link,
                        'iniciales': iniciales.upper(),
                    }
                    message = get_template('email_confirmation.html').render(Context(ctx))
                    msg = EmailMessage(email_subject, message, to=to)
                    msg.content_subtype = 'html'
                    if (request.user.groups.first().name == "super_admin")\
                       or request.user.groups.first().name == "admin":
                        msg.attach('manual_corredores.pdf',
                           open('cotizador_acerta/static/pdf/manual_corredores.pdf','rb').read(),
                           'application/pdf')
                    else:
                        msg.attach('manual_vendedores.pdf',
                           open('cotizador_acerta/static/pdf/manual_vendedores.pdf','rb').read(),
                           'application/pdf')
                    msg.send()
                    # Add the user into the group: Seller or Agent.
                    if request.user.groups.first().name == "super_admin"\
                       or request.user.groups.first().name == "admin":
                        group = Group.objects.get(name='corredor')
                        user.groups.add(group)
                    else:
                        group = Group.objects.get(name='vendedor')
                        user.groups.add(group)

                    # Add relationship Seller-Agent. If required.
                    if group.name == "vendedor":
                        new_relat = CorredorVendedor(corredor=request.user,
                                                     vendedor=user)
                        new_relat.save()
                    if request.user.groups.first().name == "super_admin"\
                       or request.user.groups.first().name == "admin":
                        if form.cleaned_data['ruc'] or form.cleaned_data['licencia']:
                            datos_corredor = DatosCorredor(user=user,
                                                           ruc=request.POST['ruc'],
                                                           licencia=request.POST['licencia'],
                                                           razon_social=form.cleaned_data['razon_social'])
                        else:
                            datos_corredor = DatosCorredor(user=user,
                                                           ruc='-',
                                                           licencia='-',
                                                           razon_social='-')
                        datos_corredor.save()
                    return HttpResponseRedirect(
                        reverse_lazy('register'))
                else:
                    if request.user.groups.first().name == "super_admin"\
                       or request.user.groups.first().name == "admin":
                        context = {'form': form}
                        return render_to_response(
                            'registro_corredor.html', context,
                            context_instance=RequestContext(request))
                    else:
                        context = {'form': form}
                        return render_to_response(
                            'register.html', context,
                            context_instance=RequestContext(request))
            else:
                if request.user.groups.first().name == "super_admin"\
                   or request.user.groups.first().name == "admin":
                    form = CorredorCreateForm()
                    context = {'form': form}
                    return render_to_response(
                        'registro_corredor.html', context,
                        context_instance=RequestContext(request))
                else:
                    form = UserCreateForm()
                    context = {'form': form}
                    return render_to_response(
                        'register.html', context,
                        context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(
                reverse_lazy('vehiculo'))
    else:
        return HttpResponseRedirect(
            reverse_lazy('login'))


def authenticate_user(username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(email=username)
            if user is not None:
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
                if user is not None:
                    return user
            except User.DoesNotExist:
                return None


def login_request(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(
            reverse_lazy('vehiculo'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_auth = authenticate_user(username, password)
            if user_auth is not None:
                if user_auth.is_active:
                    user = authenticate(username=user_auth.username,
                                        password=password)
                    if user:
                        login(request, user)
                        return HttpResponseRedirect(
                            reverse_lazy('vehiculo'))
                    else:
                        form.add_error(
                            None, "Tu correo o contraseña no son correctos")
                else:
                    form.add_error(None, "Aún no has confirmado tu correo.")
                    user = None
            else:
                form.add_error(
                    None, "Tu correo o contraseña no son correctos")
    else:
        form = LoginForm()
    context = {'form': form, 'host': request.get_host()}
    return render_to_response('login.html', context,
                              context_instance=RequestContext(request))


def editAccount(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('/'))

    template_name = 'edit_account.html'

    if request.method == 'GET':
        form = UserEditForm(initial={'username': request.user.username,
                                     'email': request.user.email})
        return render(request, template_name, {'form': form})
    elif request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse_lazy('home'))

        return render(request, template_name, {'form': form})


def register_confirm(request, activation_key):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('vehiculo'))

    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)
    user = user_profile.user

    if user.is_active:
        return HttpResponseRedirect(reverse_lazy('vehiculo'))

    if user_profile.key_expires < timezone.now():
        return HttpResponseRedirect(reverse_lazy('generate_key',
                                                 kwargs={'pk': user.pk}))

    user.is_active = True
    user.save()
    return render_to_response('cuenta_activada.html')


def generate_key(request, pk):

    if request.user.is_authenticated():
        HttpResponseRedirect(reverse_lazy('vehiculo'))

    user = User.objects.get(pk=pk)
    UserProfile.objects.filter(user=user).delete()
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt + user.email).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    new_profile = UserProfile(user=user, activation_key=activation_key,
                              key_expires=key_expires)
    new_profile.save()
    email_subject = 'Bienvenido(a) a Acerta Seguros'
    to = [user.email]
    link = 'http://' + request.get_host() + '/accounts/confirm/' + activation_key + '/' + user.pk
    if user.first_name and user.last_name:
        iniciales = user.first_name[0] + user.last_name[0]
    else:
        iniciales = user.username[:2]
    ctx = {
        'user': user,
        'link': link,
        'iniciales': iniciales.upper(),
    }
    message = get_template('email_confirmation.html').render(Context(ctx))
    msg = EmailMessage(email_subject, message, to=to)
    msg.content_subtype = 'html'
    msg.send()
    return render_to_response('reenvio_activacion.html')


@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    post_reset_redirect = reverse_lazy('password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


class EditUser(LoginRequiredMixin, GroupRequiredMixin, generic.UpdateView):
    template_name = "update_user_form.html"
    model = User
    form_class = UserEditForm
    context_object_name = "usuario"
    success_url = 'corredor_vendedor_detail'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        datos = DatosCorredor.objects.get(user=self.object)
        initial = self.initial.copy()
        if datos:
            if datos.ruc != '-':
                initial['ruc'] = datos.ruc
            if datos.licencia != '-':
                initial['licencia'] = datos.licencia
            if datos.razon_social != '-':
                initial['razon_social'] = datos.razon_social
        return initial

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = User.objects.get(email=form.cleaned_data['email'])
        corredor = DatosCorredor.objects.get(user=user)
        if form.cleaned_data['licencia']:
            corredor.licencia = form.cleaned_data['licencia']
        if form.cleaned_data['ruc']:
            corredor.ruc = form.cleaned_data['ruc']
        if form.cleaned_data['razon_social']:
            corredor.razon_social = form.cleaned_data['razon_social']
        corredor.save()
        return HttpResponseRedirect(
            reverse_lazy(self.success_url, kwargs={'pk': user.pk}))


class EditVendedor(LoginRequiredMixin, CorredorRequiredMixin, generic.UpdateView):
    template_name = "update_vendedor_form.html"
    model = User
    form_class = VendedorEditForm
    context_object_name = "usuario"
    success_url = 'corredor_vendedor_detail'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        return HttpResponseRedirect(
            reverse_lazy(self.success_url, kwargs={'pk': user.pk}))


class EditPassword(LoginRequiredMixin, generic.UpdateView):
    template_name = "update_password_form.html"
    model = User
    form_class = UserPasswordEditForm
    context_object_name = "usuario"
    success_url = 'vehiculo'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if int(request.user.pk) != int(kwargs['pk']):
            return page_not_found(request)
        return super(EditPassword, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        return HttpResponseRedirect(
            reverse_lazy(self.success_url))


class ActivateAccount(generic.UpdateView):
    template_name = "activate_account.html"
    model = User
    form_class = UserPasswordEditForm
    context_object_name = "usuario"
    success_url = 'vehiculo'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('vehiculo'))
        user_profile = get_object_or_404(
            UserProfile, activation_key=kwargs['activation_key'])
        user = user_profile.user

        if user.is_active:
            return HttpResponseRedirect(reverse_lazy('vehiculo'))

        if user_profile.key_expires < timezone.now():
            return HttpResponseRedirect(reverse_lazy('generate_key',
                                                     kwargs={'pk': user.pk}))

        user.is_active = True
        user.save()
        return super(ActivateAccount, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        return HttpResponseRedirect(
            reverse_lazy(self.success_url))
