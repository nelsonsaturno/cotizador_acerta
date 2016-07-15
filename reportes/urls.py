from django.conf.urls import url
from reportes.views import *

urlpattern = [
    url(
        r'^$',
        CorredorListView.as_view(),
        name='corredor-list'),
]
