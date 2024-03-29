from django.conf.urls import url, patterns
from administrador.views import *
from cotizar.views import VolverVehiculo

urlpatterns = patterns(
    '',
    url(
        r'^factores/$',
        Factores.as_view(),
        name='factores'
    ),
    url(
        r'^list_sexo/$',
        ListSexo.as_view(),
        name='list_sexo'
    ),
    url(
        r'^list_sexo_history/(?P<pk>\d+)$',
        ListSexoHistory.as_view(),
        name='list_sexo_history'
    ),
    url(
        r'^admin-sexo/(?P<pk>\d+)$',
        AdminSexo.as_view(),
        name='admin_sexo'
    ),
    url(
        r'^list_historial_transito/$',
        ListHistorialTransito.as_view(),
        name='list_historial_transito'
    ),
    url(
        r'^list_historial_history/(?P<pk>\d+)$',
        ListHistorialHistory.as_view(),
        name='list_historial_history'
    ),
    url(
        r'^admin-historial-transito/(?P<pk>\d+)$',
        AdminHistorialTransito.as_view(),
        name='admin_historial_transito'
    ),
    url(
        r'^list_estado_civil/$',
        ListEstadoCivil.as_view(),
        name='list_estado_civil'
    ),
    url(
        r'^list_estado_civil_history/(?P<pk>\d+)$',
        ListEstadoCivilHistory.as_view(),
        name='list_estado_civil_history'
    ),
    url(
        r'^admin-estado-civil/(?P<pk>\d+)$',
        AdminEstadoCivil.as_view(),
        name='admin_estado_civil'
    ),
    url(
        r'^list_valor/$',
        ListValor.as_view(),
        name='list_valor'
    ),
    url(
        r'^list_valor_history/(?P<pk>\d+)$',
        ListValorHistory.as_view(),
        name='list_valor_history'
    ),
    url(
        r'^admin-valor/(?P<pk>\d+)$',
        AdminValor.as_view(),
        name='admin_valor'
    ),
    url(
        r'^list_antiguedad/$',
        ListAntiguedad.as_view(),
        name='list_antiguedad'
    ),
    url(
        r'^list_antiguedad_history/(?P<pk>\d+)$',
        ListAntiguedadHistory.as_view(),
        name='list_antiguedad_history'
    ),
    url(
        r'^admin-antiguedad/(?P<pk>\d+)$',
        AdminAntiguedad.as_view(),
        name='admin_antiguedad'
    ),
    url(
        r'^list_edad/$',
        ListEdad.as_view(),
        name='list_edad'
    ),
    url(
        r'^list_edad_history/(?P<pk>\d+)$',
        ListEdadHistory.as_view(),
        name='list_edad_history'
    ),
    url(
        r'^admin-edad/(?P<pk>\d+)$',
        AdminEdad.as_view(),
        name='admin_edad'
    ),
    url(
        r'^list_tiempo_uso/$',
        ListTiempoUso.as_view(),
        name='list_tiempo_uso'
    ),
    url(
        r'^list_tiempo_uso_history/(?P<pk>\d+)$',
        ListTiempoUsoHistory.as_view(),
        name='list_tiempo_uso_history'
    ),
    url(
        r'^admin-tiempo-uso/(?P<pk>\d+)$',
        AdminTiempoUso.as_view(),
        name='admin_tiempo_uso'
    ),
    url(
        r'^list_colision/$',
        ListColision.as_view(),
        name='list_colision'
    ),
    url(
        r'^list_colision_history/(?P<pk>\d+)$',
        ListColisionHistory.as_view(),
        name='list_colision_history'
    ),
    url(
        r'^admin-colision/(?P<pk>\d+)$',
        AdminColision.as_view(),
        name='admin_colision'
    ),
    url(
        r'^list_importacion/$',
        ListImportacion.as_view(),
        name='list_importacion'
    ),
    url(
        r'^list_importacion_history/(?P<pk>\d+)$',
        ListImportacionHistory.as_view(),
        name='list_importacion_history'
    ),
    url(
        r'^admin-importacion/(?P<pk>\d+)$',
        AdminImportacion.as_view(),
        name='admin_importacion'
    ),
    url(
        r'^list_endoso/$',
        ListEndoso.as_view(),
        name='list_endoso'
    ),
    url(
        r'^list_endoso_history/(?P<pk>\d+)$',
        ListEndosoHistory.as_view(),
        name='list_endoso_history'
    ),
    url(
        r'^admin-endoso/(?P<pk>\d+)$',
        AdminEndoso.as_view(),
        name='admin_endoso'
    ),
    url(
        r'^crear-endoso/$',
        CrearEndoso.as_view(),
        name='crear_endoso'
    ),
    url(
        r'^show-pdf/(?P<pk>\d+)$',
        DisplayPDFView.as_view(),
        name='show_pdf'
    ),
    url(
        r'^show-pdf-history/(?P<pk>\d+)$',
        DisplayPDFHistoryView.as_view(),
        name='show_pdf_history'
    ),
    url(
        r'^list_lesiones/$',
        ListLesiones.as_view(),
        name='list_lesiones'
    ),
    url(
        r'^list_lesiones_history/(?P<pk>\d+)$',
        ListLesionesHistory.as_view(),
        name='list_lesiones_history'
    ),
    url(
        r'^admin-lesiones/(?P<pk>\d+)$',
        AdminLesiones.as_view(),
        name='admin_lesiones'
    ),
    url(
        r'^list_danios/$',
        ListDanios.as_view(),
        name='list_danios'
    ),
    url(
        r'^list_danios_history/(?P<pk>\d+)$',
        ListDaniosHistory.as_view(),
        name='list_danios_history'
    ),
    url(
        r'^admin-danios/(?P<pk>\d+)$',
        AdminDanios.as_view(),
        name='admin_danios'
    ),
    url(
        r'^list_gastos/$',
        ListGastos.as_view(),
        name='list_gastos'
    ),
    url(
        r'^list_gastos_history/(?P<pk>\d+)$',
        ListGastosHistory.as_view(),
        name='list_gastos_history'
    ),
    url(
        r'^admin-gastos/(?P<pk>\d+)$',
        AdminGastos.as_view(),
        name='admin_gastos'
    ),
    url(
        r'^list_marca/$',
        ListMarca.as_view(),
        name='list_marca'
    ),
    url(
        r'^list_marca_history/(?P<pk>\d+)$',
        ListMarcaHistory.as_view(),
        name='list_marca_history'
    ),
    url(
        r'^admin-marca/(?P<pk>\d+)$',
        AdminMarca.as_view(),
        name='admin_marca'
    ),
    url(
        r'^list_modelo/(?P<pk>\d+)$',
        ListModelo.as_view(),
        name='list_modelo'
    ),
    url(
        r'^list_modelo_history/(?P<pk>\d+)$',
        ListModeloHistory.as_view(),
        name='list_modelo_history'
    ),
    url(
        r'^admin-modelo/(?P<pk>\d+)$',
        AdminModelo.as_view(),
        name='admin_modelo'
    ),
    url(
        r'^cotizar-ahora/actualizar/vehiculo/(?P<pk>\d+)/(?P<pkc>\d+)/$',
        VolverVehiculo.as_view(),
        name='volver-vehiculo'
    ),
)
