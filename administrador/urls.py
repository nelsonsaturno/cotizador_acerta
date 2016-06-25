from django.conf.urls import url, patterns
from administrador.views import *

urlpatterns = patterns(
    '',
    url(r'^dashboard/$',
        Dashboard.as_view(),
        name='dashboard'),
    url(r'^list_sexo/$',
        ListSexo.as_view(),
        name='list_sexo'),
    url(r'^admin-sexo/(?P<pk>\d+)$',
        AdminSexo.as_view(),
        name='admin_sexo'),
)
