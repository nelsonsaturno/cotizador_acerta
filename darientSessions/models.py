from django.db import models
from django.contrib.auth.models import User
import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = u'User profiles'


class CorredorVendedor(models.Model):
    corredor = models.ForeignKey(User, related_name='corredor')
    vendedor = models.ForeignKey(User, related_name='vendedor', unique=True)

    def __str__(self):
        return self.vendedor.username + ' created by ' + self.corredor.username

    class Meta:
        verbose_name_plural = u'CorredorVendedors'


class DatosCorredor(models.Model):

    user = models.OneToOneField(User)
    ruc = models.CharField(max_length=100, null=False)
    licencia = models.CharField(max_length=100, null=False)
    razon_social = models.CharField(max_length=100, null=True, blank=True)
    planes = models.CharField(
        max_length=100, default='-',
        choices=[
            ('Plan 1', 'Plan 1'),
            ('Plan 2', 'Plan 2'),
            ('Plan 3', 'Plan 3')
        ]
    )

    def __str__(self):
        return self.user.username + ' - ' + self.licencia


class PolizasCorredor(models.Model):
    user = models.OneToOneField(User)
    polizas_desde = models.PositiveIntegerField(
        null=False, blank=False, default=1)
    polizas_hasta = models.PositiveIntegerField(
        null=False, blank=False, default=50000)
    polizas = models.IntegerField(
        null=False, blank=False, default=0)

    def __str__(self):
        return self.user.username + ' - ' + str(self.polizas)