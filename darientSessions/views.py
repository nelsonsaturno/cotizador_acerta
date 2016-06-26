#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import datetime
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import *
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User
from django.views import generic
from cotizador_acerta.views_mixins import *
from darientSessions.models import UserProfile
from darientSessions.forms import UserCreateForm, LoginForm, UserEditForm


# class RegistroCorredor(LoginRequiredMixin,
#                        GroupRequiredMixin, generic.CreateView):

#     def post(self, request, *args, **kwargs):
#         form = UserCreateForm(request.POST)
#         if form.is_valid():
#             form.save()
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            # activation_key = hashlib.sha1(salt + email).hexdigest()
            # key_expires = datetime.datetime.today() + datetime.timedelta(2)
            # user = User.objects.get(username=username)
            # new_profile = UserProfile(user=user, activation_key=activation_key,
            #                           key_expires=key_expires)
            # new_profile.save()
            # email_subject = 'Account confirmation'
            # email_body ="Hey %s, thanks for signing up. To activate your account, click this link within 48hours http://%s/user/accounts/confirm/%s" %\
            #     (username, request.get_host(), activation_key)
            # send_mail(email_subject, email_body, 'acerta@darient.com',
            #           [email], fail_silently=False)
    #         return HttpResponseRedirect(
    #             reverse_lazy('login'))
    #     else:
    #         context = {'form': form}
    #         return render_to_response('register.html', context,
    #                                   context_instance=RequestContext(request))

    # def get(self, request, *args, **kwargs):
    #     form = UserCreateForm()
    #     context = {'form': form}
    #     return render_to_response('register.html', context,
    #                               context_instance=RequestContext(request))


def user_registration(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            user = User.objects.get(username=username)
            new_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()
            email_subject = 'Account confirmation'
            email_body ="Hey %s, thanks for signing up. To activate your account, click this link within 48hours http://%s/user/accounts/confirm/%s" %\
                (username, request.get_host(), activation_key)
            send_mail(email_subject, email_body, 'acerta@darient.com',
                      [email], fail_silently=False)
            return HttpResponseRedirect(
                reverse_lazy('login'))
        else:
            context = {'form': form}
            return render_to_response('register.html', context,
                                      context_instance=RequestContext(request))
    else:
        form = UserCreateForm()
        context = {'form': form}
        return render_to_response('register.html', context,
                                  context_instance=RequestContext(request))


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
               reverse_lazy('conductor'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_auth = authenticate_user(username, password)
            if user_auth is not None:
                user = authenticate(username=user_auth.username,
                                    password=password)
            else:
                form.add_error(None, "Tu correo o contraseña no son correctos")
                user = None
            if user:
                login(request, user)
                return HttpResponseRedirect(
                       reverse_lazy('conductor'))
            else:
                form.add_error(None, "Tu correo o contraseña no son correctos")
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
        HttpResponseRedirect(reverse_lazy('login'))

    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)
    user = user_profile.user

    if user_profile.key_expires < timezone.now():
        return HttpResponseRedirect(reverse_lazy('login',
                                                 kwargs={'pk': user.pk}))

    user.is_active = True
    user.save()
    return HttpResponseRedirect(
           reverse_lazy('login'))


def generate_key(request, pk):

    if request.user.is_authenticated():
        HttpResponseRedirect(reverse_lazy('login'))

    user = User.objects.get(pk=pk)
    UserProfile.objects.filter(user=user).delete()
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt + user.email).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    new_profile = UserProfile(user=user, activation_key=activation_key,
                              key_expires=key_expires)
    new_profile.save()
    email_subject = 'Account confirmation'
    email_body = "Hey %s, thanks for signing up. To activate your account, click this link within 48hours http://%s/user/accounts/confirm/%s" % \
        (user.username, request.get_host(), activation_key)
    send_mail(email_subject, email_body, 'ns@darient.com',
              [user.email], fail_silently=False)
    return HttpResponseRedirect(
           reverse_lazy('login'))
