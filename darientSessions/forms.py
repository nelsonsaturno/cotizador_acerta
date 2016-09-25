#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from random import choice
from string import ascii_lowercase, digits


def generate_random_username(length=16, chars=ascii_lowercase + digits, split=4, delimiter='-'):

    username = ''.join([choice(chars) for i in xrange(length)])

    if split:
        username = delimiter.join(
            [username[start:start+split] for start in range(0, len(username), split)])

    try:
        User.objects.get(username=username)
        return generate_random_username(
            length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        active_users = User.objects.filter(
            email=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = 'Reestablece tu contraseña'
            # Email subject *must not* contain newlines
            message = get_template(
                'registrations/html_password_reset_email.html').render(Context(c))
            msg = EmailMessage(
                subject, message, to=[user.email], from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()


class UserCreateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

        error_messages = {
            'first_name': {
                'required': "Este campo es requerido"
            },
            'last_name': {
                'required': "Este campo es requerido"
            }
        }

        widgets = {
            'email': forms.TextInput(attrs={'required': 'true'}),
            'first_name': forms.TextInput(attrs={'required': 'true'}),
            'last_name': forms.TextInput(attrs={'required': 'true'})
        }

        labels = {
            'email': 'Correo',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).count() != 0:
            raise forms.ValidationError(u'Este correo ya existe.')
        return email

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = generate_random_username()
        user.is_active = 0
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        return user


class CorredorCreateForm(forms.ModelForm):
    licencia = forms.CharField(required=False,
                               label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Nro. de Licencia'}))
    ruc = forms.CharField(required=False,
                          label="",
                          widget=forms.TextInput(attrs={'placeholder': 'RUC'}))
    razon_social = forms.CharField(
                                    required=False,
                                    label="",
                                     widget=forms.TextInput(attrs={'placeholder': 'Razón Social'}))
    planes = forms.MultipleChoiceField(choices=[
                                        ('Plan 1', 'Plan 1'),
                                        ('Plan 2', 'Plan 2'),
                                        ('Plan 3', 'Plan 3')
                                        ],
                                widget=forms.CheckboxSelectMultiple
                                )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

        error_messages = {
            'first_name': {
                'required': "Este campo es requerido"
            },
            'last_name': {
                'required': "Este campo es requerido"
            }
        }

        widgets = {
            'email': forms.TextInput(attrs={'required': 'true'}),
            'first_name': forms.TextInput(attrs={'required': 'true'}),
            'last_name': forms.TextInput(attrs={'required': 'true'})
        }

        labels = {
            'email': 'Correo',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

    def clean_licencia(self):
        licencia = self.cleaned_data.get('licencia')
        if len(licencia) > 100:
            raise forms.ValidationError(u'Este campo no puede superar los 100 caracteres.')
        return licencia

    def clean_razon_social(self):
        razon_social = self.cleaned_data.get('razon_social')
        if len(razon_social) > 100:
            raise forms.ValidationError(u'Este campo no puede superar los 100 caracteres.')
        return razon_social

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if len(ruc) > 100:
            raise forms.ValidationError(u'Este campo no puede superar los 100 caracteres.')
        return ruc

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).count() != 0:
            raise forms.ValidationError(u'Este correo ya existe.')
        return email

    def save(self, commit=True):
        user = super(CorredorCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = generate_random_username()
        user.is_active = 0
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        return user


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=60, required=True,
        label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Clave'}), required=True, label='')


class UserEditForm(forms.ModelForm):

    licencia = forms.CharField(required=False,
                               label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Nro. de Licencia'}))
    ruc = forms.CharField(required=False,
                          label="",
                          widget=forms.TextInput(attrs={'placeholder': 'RUC'}))
    razon_social = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Razón Social'}))
    username = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

        error_messages = {
            'first_name': {
                'required': "Este campo es requerido"
            },
            'last_name': {
                'required': "Este campo es requerido"
            }
        }

        widgets = {
            'email': forms.TextInput(attrs={'required': 'true'}),
            'first_name': forms.TextInput(attrs={'required': 'true'}),
            'last_name': forms.TextInput(attrs={'required': 'true'})
        }

        labels = {
            'email': 'Correo',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

    def clean_licencia(self):
        licencia = self.cleaned_data.get('licencia')
        if len(licencia) > 100:
            raise forms.ValidationError(u'Este campo no puede superar los 100 caracteres.')
        return licencia

    def clean_razon_social(self):
        razon_social = self.cleaned_data.get('razon_social')
        if len(razon_social) > 100:
            raise forms.ValidationError(u'Este campo no puede superar los 100 caracteres.')
        return razon_social

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if len(ruc) > 100:
            raise forms.ValidationError(u'Este campo no puede superar los 100 caracteres.')
        return ruc

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        user_1 = User.objects.filter(email=email)
        if len(user_1) == 0:
            return self.cleaned_data
        user_2 = User.objects.get(pk=username)
        if user_1[0].pk != user_2.pk:
            raise forms.ValidationError(u'Este correo ya existe.')
        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()
        return user


class VendedorEditForm(forms.ModelForm):

    username = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

        error_messages = {
            'first_name': {
                'required': "Este campo es requerido"
            },
            'last_name': {
                'required': "Este campo es requerido"
            }
        }

        widgets = {
            'email': forms.TextInput(attrs={'required': 'true'}),
            'first_name': forms.TextInput(attrs={'required': 'true'}),
            'last_name': forms.TextInput(attrs={'required': 'true'})
        }

        labels = {
            'email': 'Correo',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        user_1 = User.objects.filter(email=email)
        if len(user_1) == 0:
            return self.cleaned_data
        user_2 = User.objects.get(pk=username)
        if user_1[0].pk != user_2.pk:
            raise forms.ValidationError(u'Este correo ya existe.')
        return self.cleaned_data

    def save(self, commit=True):
        user = super(VendedorEditForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()
        return user


class UserPasswordEditForm(forms.ModelForm):
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repetir contraseña'}),
                                label="")

    class Meta:
        model = User
        fields = ('password',)

        error_messages = {
            'password': {
                'required': "Este campo es requerido"
            },
            'password2': {
                'required': "Este campo es requerido"
            }
        }

        widgets = {
            'password': forms.PasswordInput()
        }

        labels = {
            'password': 'Contraseña'
        }

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password == password2:
            return self.cleaned_data
        else:
            raise forms.ValidationError(u'Ambas contraseñas deben coincidir.')

    def save(self, commit=True):
        user = super(UserPasswordEditForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user
