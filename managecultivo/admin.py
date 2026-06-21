from django.contrib import admin
from .models import (
    ZonaAgricola, Personal, Cultivo, Actividad, Insumo,
    CultivoActividad, CultivoActividadInsumo, CompraInsumo,
    Ciclo, CicloActividad, CicloActividadInsumo,
    CicloActividadPersonal, UnidadTiempo, CicloMonitoreo, CultivoActividadPersonal
)

admin.site.register(ZonaAgricola)
admin.site.register(Personal)
admin.site.register(Cultivo)
admin.site.register(Actividad)
admin.site.register(Insumo)
admin.site.register(CultivoActividad)
admin.site.register(CultivoActividadInsumo)
admin.site.register(CultivoActividadPersonal)
admin.site.register(CompraInsumo)
admin.site.register(Ciclo)
admin.site.register(CicloActividad)
admin.site.register(CicloActividadInsumo)
admin.site.register(CicloActividadPersonal)
admin.site.register(UnidadTiempo)
admin.site.register(CicloMonitoreo)

# Register your models here.
