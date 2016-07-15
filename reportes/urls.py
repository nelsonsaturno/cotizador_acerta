from django.conf.urls import url, patterns
from reportes.views import *

urlpatterns = patterns(
    '',
    url(
        r'^corredores/$',
        CorredorListView.as_view(),
        name='corredor-list'),
)
