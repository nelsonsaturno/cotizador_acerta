from django.conf.urls import url, patterns
from polizas.views import *

urlpatterns = patterns(
    '',
    url(
        r'^solicitar/(?P<pk>\d+)/$',
        SolicitudPolizaView.as_view(),
        name='solicitar'
    ),
    url(
        r'^detalles/(?P<pk>\d+)/$',
        DetallePoliza.as_view(),
        name='detalles-poliza'
    ),
    url(
        r'^prueba/$',
        Test.as_view(),
        name='prueba'
    ),
    url(
        r'^prueba/generacion$',
        GeneracionPDF.as_view(),
        name='generacion'
    ),
    url(
        r'^realizar-pago/$',
        PagoTarjeta.as_view(),
        name='realizar_pago'
    ),
    url(
        r'^confirmacion-pago/$',
        ConfirmacionPago.as_view(),
        name='confirmacion_pago'
    ),
    url(
        r'^generarPDF/(?P<pk>\d+)/$',
        GeneracionPDFPolizas.as_view(),
        name='generacion-pdf-polizas'
    ),
)
