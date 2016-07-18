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
    ruc = models.CharField(max_length=20, null=False)
    licencia = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.user.username + ' - ' + self.licencia
