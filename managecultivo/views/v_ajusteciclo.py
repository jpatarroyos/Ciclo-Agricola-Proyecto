from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import Ciclo, CicloActividad, CicloActividadInsumo, Actividad, Insumo, Personal, CicloActividadPersonal
import calendar

def ajustar_ciclo(request, ciclo_id):
    ciclo = get_object_or_404(Ciclo, pk=ciclo_id)

    inicio_mes = ciclo.fecha_inicio.replace(day=1)
    fin_mes = ciclo.fecha_fin.replace(day=1)

    # Determinar mes actual desde querystring o usar fecha_inicio del ciclo
    mes_str = request.GET.get("mes")
    if mes_str:
        try:
            year, month = map(int, mes_str.split("-"))
            fecha_base = datetime(year, month, 1).date()
        except ValueError:
            fecha_base = inicio_mes
    else:
        fecha_base = inicio_mes

    # Convertir a índice de meses para comparar
    inicio_index = inicio_mes.year * 12 + inicio_mes.month
    fin_index = fin_mes.year * 12 + fin_mes.month
    base_index = fecha_base.year * 12 + fecha_base.month

    if base_index < inicio_index:
        fecha_base = inicio_mes
    if base_index > fin_index:
        fecha_base = fin_mes

    # Generar calendario del mes seleccionado
    actividades_ciclo = CicloActividad.objects.filter(id_ciclo=ciclo).order_by("fecha_programada")

    cal = calendar.Calendar(firstweekday=0)
    semanas = cal.monthdatescalendar(fecha_base.year, fecha_base.month)

    calendario = []
    for semana in semanas:
        dias = []
        for dia in semana:
            acts_dia = [a for a in actividades_ciclo if a.fecha_programada == dia]
            dias.append({"fecha": dia, "actividades": acts_dia})
        calendario.append(dias)

    # Si viene parámetro fecha, filtrar actividades de ese día
    actividades_dia = CicloActividad.objects.none()
    fecha_seleccionada = None
    if "fecha" in request.GET:
        fecha_str = request.GET.get("fecha")
        try:
            fecha_seleccionada = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            actividades_dia = CicloActividad.objects.filter(
                id_ciclo=ciclo,
                fecha_programada=fecha_seleccionada
            )
        except ValueError:
            pass

    # === MANEJO DE PETICIONES POST ===
    if request.method == "POST":
        if "add_actividad" in request.POST:
            fecha_str = request.POST.get("fecha")
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            id_actividad = request.POST.get("id_actividad")
            color = request.POST.get("color")

            CicloActividad.objects.create(
                id_ciclo=ciclo,
                id_actividad_id=id_actividad,
                fecha_programada=fecha,
                color=color,
                registrado_por=request.user
            )
            messages.success(request, "Actividad agregada correctamente")
            return redirect("ajustar_ciclo", ciclo_id=ciclo.id_ciclo)

        if "add_insumo" in request.POST:
            actividad_id = request.POST.get("actividad_id")
            insumo_id = request.POST.get("id_insumo")
            cantidad = request.POST.get("cantidad_utilizada")
            CicloActividadInsumo.objects.create(
                actividad_ciclo_id=actividad_id,
                id_insumo_id=insumo_id,
                cantidad_utilizada=cantidad,
                registrado_por=request.user
            )
            return redirect("ajustar_ciclo", ciclo_id=ciclo.id_ciclo)

        if "add_personal" in request.POST:
            actividad_id = request.POST.get("actividad_id")
            personal_id = request.POST.get("id_personal")
            CicloActividadPersonal.objects.create(
                actividad_ciclo_id=actividad_id,
                personal_id=personal_id
            )
            messages.success(request, "Personal asignado correctamente")            
            return redirect("ajustar_ciclo", ciclo_id=ciclo.id_ciclo)

        if "borrar_actividad" in request.POST:
            actividad_id = request.POST.get("actividad_id")
            actividad_ciclo = get_object_or_404(CicloActividad, pk=actividad_id)
            actividad_ciclo.delete()
            messages.success(request, "Actividad eliminada correctamente")
            return redirect("ajustar_ciclo", ciclo_id=ciclo.id_ciclo)
        # === ACTUALIZACIÓN CONTROLADA POR CHECKBOX DE INSUMOS ===
        if "editar_insumos" in request.POST:
            actividad_id = request.POST.get("actividad_id")
            # Obtenemos la lista de los IDs de insumos cuyos checkboxes fueron marcados
            insumos_chequeados = request.POST.getlist("insumos_seleccionados")
            
            # 1. Borrar todas las asignaciones previas de esta actividad en particular
            CicloActividadInsumo.objects.filter(actividad_ciclo_id=actividad_id).delete()
            
            # 2. Iterar únicamente sobre los insumos seleccionados con el check
            for insumo_id in insumos_chequeados:
                # Extraemos la cantidad correspondiente al insumo actual
                cantidad_str = request.POST.get(f"cantidad_{insumo_id}")
                
                if cantidad_str:
                    try:
                        cantidad_float = float(cantidad_str)
                        # Opcional: Si el check está marcado pero dejó la cantidad vacía o en 0, le asignamos 0 o validamos
                        if cantidad_float >= 0:
                            CicloActividadInsumo.objects.create(
                                actividad_ciclo_id=actividad_id,
                                id_insumo_id=insumo_id,
                                cantidad_utilizada=cantidad_float,
                                registrado_por=request.user
                            )
                    except ValueError:
                        pass # Protección ante caracteres raros en el casillero numérico
            
            messages.success(request, "Insumos y cantidades actualizados con éxito")

            # 3. Redirección limpia conservando la posición del calendario
            response = redirect("ajustar_ciclo", ciclo_id=ciclo.id_ciclo)
            mes_actual_url = request.GET.get("mes", "")
            fecha_seleccionada_url = request.GET.get("fecha", "")
            
            url_destino = ""
            if mes_actual_url:
                url_destino += f"&mes={mes_actual_url}"
            if fecha_seleccionada_url:
                url_destino += f"&fecha={fecha_seleccionada_url}"
                
            if url_destino:
                response['Location'] += f"?{url_destino.lstrip('&')}"
                
            return response

        # === CORRECCIÓN AQUÍ: Dentro del bloque POST ===
        if "update_personal" in request.POST:
            actividad_id = request.POST.get("actividad_id")
            seleccionados = request.POST.getlist("id_personal")

            # Borrar asignaciones anteriores de esta actividad
            CicloActividadPersonal.objects.filter(actividad_ciclo_id=actividad_id).delete()

            # Crear las nuevas asignaciones
            for pid in seleccionados:
                if pid:
                    CicloActividadPersonal.objects.create(
                        actividad_ciclo_id=actividad_id,
                        personal_id=pid
                    )
            
            messages.success(request, "Personal actualizado correctamente")

            # Construimos la respuesta redirigiendo a la misma vista con los parámetros GET
            response = redirect("ajustar_ciclo", ciclo_id=ciclo.id_ciclo)
            
            mes_actual_url = request.GET.get("mes", "")
            fecha_seleccionada_url = request.GET.get("fecha", "")
            
            url_destino = ""
            if mes_actual_url:
                url_destino += f"&mes={mes_actual_url}"
            if fecha_seleccionada_url:
                url_destino += f"&fecha={fecha_seleccionada_url}"
                
            if url_destino:
                response['Location'] += f"?{url_destino.lstrip('&')}"
                
            return response

    # Recuperar asignaciones para la vista (GET)
    asignaciones = CicloActividadPersonal.objects.filter(
        actividad_ciclo__id_ciclo=ciclo
    )
  
    return render(request, "ajustar_ciclo.html", {
        "ciclo": ciclo,
        "calendario": calendario,
        "mes_actual": fecha_base,
        "actividades_lista": Actividad.objects.all(),
        "insumos": Insumo.objects.all(),
        "actividades": actividades_dia,
        "fecha_seleccionada": fecha_seleccionada,
        "personal_lista": Personal.objects.all(),   
        "asignaciones": asignaciones,        
    })
