from django.conf.urls import url, patterns
from cotizar.views import *

urlpatterns = patterns(
    '',
    url(r'^cotizar-ahora/$',
        CotizarAhora.as_view(),
        name='cotiza_ahora'),
    url(r'^cotizar-ahora/conductor/$',
        Conductor.as_view(),
        name='conductor'),
    url(r'^cotizar-ahora/vehiculo/$',
        Vehiculo.as_view(),
        name='vehiculo'),
    url(r'^cotizar-ahora/planes/(?P<pk>\d+)/(?P<pk2>\d+)/(?P<pk3>\d+)/(?P<pk4>\d+)$',
        VerPlanes.as_view(),
        name='ver_planes'),
    url(r'^cotizar-ahora/detalle-cotizacion/(?P<pk>\d+)$',
        DetalleCotizacion.as_view(),
        name='detalle_cotizacion'),
)
