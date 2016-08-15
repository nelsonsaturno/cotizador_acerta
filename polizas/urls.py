from django.conf.urls import url, patterns
from polizas.views import *

urlpatterns = patterns(
    '',
    url(r'^solicitud/$',
        SolicitudPoliza.as_view(),
        name='solicitar'),
)