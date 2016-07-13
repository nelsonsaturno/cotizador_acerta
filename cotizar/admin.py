from django.contrib import admin
from cotizar.models import *


class ModeloAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'marca',
        'descuento',
        'recargo',
        'created_at',
        'updated_at'
    )
    search_fields = (
        'id',
        'nombre',
        'marca',
        'descuento',
        'recargo',
        'created_at',
        'updated_at'
    )

admin.site.register(ConductorVehiculo)
admin.site.register(Marca)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(Cotizacion)
