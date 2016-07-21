#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User


class UserCreateForm(forms.ModelForm):
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repetir contraseña'}),
                                label="")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "username")

        error_messages = {
            'username': {
                'required': "El correo es requerido."
            }
        }

        widgets = {
            'password': forms.PasswordInput(),
            'username': forms.HiddenInput(attrs={'required': 'false'}),
            'email': forms.TextInput(attrs={'required': 'true'})
        }

        labels = {
            'email': 'Correo',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'password': 'Contraseña',
        }

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password == password2:
            return self.cleaned_data
        else:
            raise forms.ValidationError(u'Ambas contraseñas deben coincidir.')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username).count() != 0:
            raise forms.ValidationError(u'Este correo ya existe.')
        return email

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = 0
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        else:
            return user


class CorredorCreateForm(forms.ModelForm):
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repetir contraseña'}),
                                label="")
    licencia = forms.CharField(required=True,
                               label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Nro. de Licencia'}))
    ruc = forms.CharField(required=True,
                          label="",
                          widget=forms.TextInput(attrs={'placeholder': 'RUC'}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "username")

        error_messages = {
            'username': {
                'required': "El correo es requerido."
            }
        }

        widgets = {
            'password': forms.PasswordInput(),
            'username': forms.HiddenInput(attrs={'required': 'false'}),
            'email': forms.TextInput(attrs={'required': 'true'})
        }

        labels = {
            'email': 'Correo',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'password': 'Contraseña',
        }

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password == password2:
            return self.cleaned_data
        else:
            raise forms.ValidationError(u'Ambas contraseñas deben coincidir.')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username).count() != 0:
            raise forms.ValidationError(u'Este correo ya existe.')
        return email

    def save(self, commit=True):
        user = super(CorredorCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = 0
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        else:
            return user


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=60, required=True,
        label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Clave'}), required=True, label='')


class UserEditForm(forms.ModelForm):

    licencia = forms.CharField(required=True,
                               label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Nro. de Licencia'}))
    ruc = forms.CharField(required=True,
                          label="",
                          widget=forms.TextInput(attrs={'placeholder': 'RUC'}))
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

        error_messages = {
            'email': {
                'required': "El correo es requerido."
            }
        }

        widgets = {
            'username': forms.HiddenInput(attrs={'required': 'false'}),
            'email': forms.TextInput(attrs={'required': 'true'})
        }

        labels = {
            'email': 'Correo',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.save()
        return user
