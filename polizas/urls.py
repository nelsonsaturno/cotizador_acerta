from django.conf.urls import url, patterns
from polizas.views import *

urlpatterns = patterns(
    '',
    url(
        r'^solicitar/(?P<pk>\d+)/$',
        SolicitudPoliza.as_view(),
        name='solicitar'
    ),
)
