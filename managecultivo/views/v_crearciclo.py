from datetime import timedelta, datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Cultivo, Ciclo, CultivoActividad, CicloActividad, ZonaAgricola, CicloActividadInsumo, CicloActividadPersonal

import calendar
def crear_ciclo(request):
    cultivos = Cultivo.objects.all()
    zonas = ZonaAgricola.objects.all()
    ciclo = None

    if request.method == "POST":
        cultivo_id = request.POST["id_cultivo"]
        zona_id = request.POST["id_zonaagricola"]
        fecha_inicio = datetime.strptime(request.POST["fecha_inicio"], "%Y-%m-%d").date()

        cultivo = Cultivo.objects.get(pk=cultivo_id)
        fecha_fin = fecha_inicio + timedelta(days=cultivo.tiempo_agricola)

        # Validaciones de solapamiento (como ya tienes)
        ciclos_existentes = Ciclo.objects.filter(id_cultivo=cultivo, id_zonaagricola_id=zona_id)
        for c in ciclos_existentes:
            if (fecha_inicio <= c.fecha_fin and fecha_inicio >= c.fecha_inicio) \
               or (fecha_fin >= c.fecha_inicio and fecha_fin <= c.fecha_fin) \
               or (fecha_inicio <= c.fecha_inicio and fecha_fin >= c.fecha_fin):
                messages.error(request, f"Ya existe un ciclo de {cultivo.descripcion} en la zona seleccionada entre {c.fecha_inicio} y {c.fecha_fin}")
                return render(request, "crear_ciclo.html", {
                    "cultivos": cultivos,
                    "zonas": zonas,
                    "ciclo": None
                })

        # Crear ciclo nuevo
        ciclo = Ciclo.objects.create(
            id_cultivo=cultivo,
            id_zonaagricola_id=zona_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            cantidad_produccion=0,
            registrado_por=request.user
        )

        # Crear actividades del ciclo según frecuencia (como ya tienes)
        actividades = CultivoActividad.objects.filter(id_cultivo=cultivo)
        for act in actividades:
            if act.frecuencia.descripcion.lower() == "1 vez":
                dias_act = [act.dia_inicio]
            elif act.frecuencia.descripcion.lower() == "diario":
                dias_act = range(act.dia_inicio, cultivo.tiempo_agricola + 1)
            elif act.frecuencia.descripcion.lower() == "semanal":
                dias_act = range(act.dia_inicio, cultivo.tiempo_agricola + 1, 7)
            elif act.frecuencia.descripcion.lower() == "mensual":
                dias_act = range(act.dia_inicio, cultivo.tiempo_agricola + 1, 30)
            else:
                dias_act = [act.dia_inicio]

            for d in dias_act:
                fecha_prog = fecha_inicio + timedelta(days=d-1)
                actividad_ciclo = CicloActividad.objects.create(
                    id_ciclo=ciclo,
                    id_actividad=act.id_actividad,
                    fecha_programada=fecha_prog,
                    color=act.color,
                    registrado_por=request.user
                )
                for insumo in act.fk_CultivoActividadInsumo1.all():
                    CicloActividadInsumo.objects.create(
                        actividad_ciclo=actividad_ciclo,
                        id_insumo=insumo.id_insumo,
                        cantidad_utilizada=insumo.cantidad_sugerida,
                        registrado_por=request.user
                    )
                for personal_rel  in act.fk_CultivoActividadPersonal_Base.all():
                    CicloActividadPersonal.objects.create(
                        actividad_ciclo=actividad_ciclo,
                        personal=personal_rel.id_personal
                    )

        # Solo aquí haces el redirect, porque ya existe ciclo
        return redirect("ajustar_ciclo", ciclo_id=ciclo.id_ciclo)

    # ✅ En GET solo muestras el formulario, sin redirect
    return render(request, "crear_ciclo.html", {
        "cultivos": cultivos,
        "zonas": zonas,
        "ciclo": ciclo
    })
