from django.conf.urls import url, patterns
from reportes.views import *

urlpatterns = patterns(
    '',
    url(
        r'^corredores/$',
        CorredorVendedorListView.as_view(),
        name='corredor-vendedor-list'),
)
