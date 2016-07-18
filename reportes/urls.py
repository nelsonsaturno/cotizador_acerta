from django.conf.urls import url, patterns
from reportes.views import *

urlpatterns = patterns(
    '',
    url(
        r'^corredores/$',
        CorredorVendedorListView.as_view(),
        name='corredor-vendedor-list'),
    url(
        r'^corredores/detail/(?P<pk>\d+)/$',
        CorredorVendedorDetailView.as_view(),
        name='corredor_vendedor_detail'),
    url(
        r'^vendedores/$',
        VendedorListView.as_view(),
        name='vendedor_list'),
    url(
        r'^cotizaciones/$',
        CotizacionesListView.as_view(),
        name='cotizaciones_list'),
    url(
        r'^cotizaciones/detalle/(?P<pk>\d+)/$',
        CotizacionesDetailView.as_view(),
        name='cotizaciones_details'),
)
