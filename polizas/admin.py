from django.contrib import admin
from polizas.models import *


class SolicitudAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cotizacion',
    )
    search_fields = (
        'id',
        'cotizacion',
    )


class ReferenciaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
    )
    search_fields = (
        'id',
        'nombre',
    )


class ExtraDatosAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'conductor',
    )
    search_fields = (
        'id',
        'conductor',
    )


admin.site.register(SolicitudPoliza, SolicitudAdmin)
admin.site.register(Referencia, ReferenciaAdmin)
admin.site.register(ExtraDatosCliente, ExtraDatosAdmin)
