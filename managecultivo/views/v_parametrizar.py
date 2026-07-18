from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages

from ..models import Cultivo,Actividad, CultivoActividad, CultivoActividadPersonal,Insumo,CultivoActividadInsumo, Personal, UnidadTiempo

@login_required
# filtra la tabla
def parametrizar_cultivo(request):
    cultivo_id = request.GET.get("cultivo")
    semana_actual = int(request.GET.get("semana", 1))  # semana seleccionada, por defecto 1
    actividades = []
    cultivo_seleccionado = None
    semanas = []
    actividades_planeadas = []

    if cultivo_id:
        try:
            cultivo_seleccionado = Cultivo.objects.get(pk=cultivo_id)
            actividades = CultivoActividad.objects.filter(id_cultivo=cultivo_seleccionado)

            dias = list(range(1, cultivo_seleccionado.tiempo_agricola + 1))
            todas_semanas = [dias[i:i+7] for i in range(0, len(dias), 7)]

            # Mostrar solo 5 semanas a partir de la semana_actual
            inicio = (semana_actual - 1) * 5
            semanas = todas_semanas[inicio:inicio+5]

            # Calcular actividades_planeadas según frecuencia (como ya lo tienes)
            for act in actividades:
                if act.frecuencia.descripcion.lower() == "1 vez":
                    dias_act = [act.dia_inicio]
                elif act.frecuencia.descripcion.lower() == "diario":
                    dias_act = range(act.dia_inicio, cultivo_seleccionado.tiempo_agricola + 1)
                elif act.frecuencia.descripcion.lower() == "semanal":
                    dias_act = range(act.dia_inicio, cultivo_seleccionado.tiempo_agricola + 1, 7)
                elif act.frecuencia.descripcion.lower() == "mensual":
                    dias_act = range(act.dia_inicio, cultivo_seleccionado.tiempo_agricola + 1, 30)
                else:
                    dias_act = [act.dia_inicio]

                for d in dias_act:
                    actividades_planeadas.append({"dia": d, "actividad": act})

        except Cultivo.DoesNotExist:
            cultivo_seleccionado = None

    context = {
        "cultivos": Cultivo.objects.all(),
        "actividades_lista": Actividad.objects.all(),
        "unidades": UnidadTiempo.objects.all(),
        "insumos": Insumo.objects.all(),
        "personal_lista": Personal.objects.all(),
        "tipos": Insumo.TIPOS,   # 🔹 aquí pasas los choices        
        "actividades": actividades,
        "cultivo_seleccionado": cultivo_seleccionado,
        "semanas": semanas,
        "semana_actual": semana_actual,
        "actividades_planeadas": actividades_planeadas,
    }
    return render(request, "parametrizar_cultivo.html", context)

@login_required
def crear_cultivo(request):
    if request.method == "POST":
        descripcion = request.POST.get("descripcion")
        tiempo_agricola = request.POST.get("tiempo_agricola")
        Cultivo.objects.create(
            descripcion=descripcion,
            tiempo_agricola=tiempo_agricola,
            registrado_por=request.user
        )
    return redirect("parametrizar_cultivo")


@login_required
def crear_actividad(request):
    if request.method == "POST":
        descripcion = request.POST.get("descripcion")
        prioridad = request.POST.get("prioridad")  
        Actividad.objects.create(
            descripcion=descripcion,
            prioridad=prioridad,   
            registrado_por=request.user
        )
    return redirect("parametrizar_cultivo")

@login_required
def crear_insumo(request):
    if request.method == "POST":
        descripcion = request.POST.get("descripcion")
        cantidad_existente = request.POST.get("cantidad_existente")
        tipo = request.POST.get("tipo")

        Insumo.objects.create(
            descripcion=descripcion,
            cantidad_existente=cantidad_existente,
            tipo=tipo,
            registrado_por=request.user
        )
        return redirect("parametrizar_cultivo")

    # Si es GET, pasamos los choices al template
    tipos = Insumo.TIPOS
    return render(request, "crear_insumo.html", {"tipos": tipos})


@login_required
def crear_actividadcultivo(request):
    if request.method == "POST":
        print(request.POST)  
        cultivo_id = request.POST.get("id_cultivo")
        actividad_id = request.POST.get("id_actividad")
        dia_inicio = int(request.POST["dia_inicio"])
        frecuencia_id = request.POST["frecuencia"]
        min_personas = int(request.POST["min_personas"])
        max_personas = int(request.POST["max_personas"])        
        color = request.POST.get("color", "#000000")
        lista_cedulas = request.POST.getlist("personal_encargado")

        # 1. Crear ActividadCultivo
        act_cultivo = CultivoActividad.objects.create(
            id_cultivo_id=cultivo_id,
            id_actividad_id=actividad_id,
            dia_inicio=dia_inicio,
            frecuencia_id=frecuencia_id,
            min_personas= min_personas,
            max_personas= max_personas,            
            color=color,            
            registrado_por=request.user
        )

        # 2. Procesar insumos seleccionados
        insumos_seleccionados = request.POST.getlist("insumos")
        for insumo_id in insumos_seleccionados:
            cantidad = request.POST.get(f"cantidad_{insumo_id}")
            if cantidad:  # solo si se ingresó cantidad
                CultivoActividadInsumo.objects.create(
                    actividad_cultivo=act_cultivo,
                    id_insumo_id=insumo_id,
                    cantidad_sugerida=cantidad,
                    registrado_por=request.user
                )

        # 3. Procesar personal seleccionado

        for cedula in lista_cedulas:
            CultivoActividadPersonal.objects.create(
                actividad_cultivo=act_cultivo,
                id_personal_id=cedula  # Al usar '_id' podemos pasar directamente el string de la cédula
            )

    messages.success(request, "Actividad guardada correctamente.")
    return redirect("parametrizar_cultivo")

@login_required
def borrar_actividadcultivo(request, pk):
    actividad = get_object_or_404(CultivoActividad, pk=pk)
    actividad.delete()
    return redirect("parametrizar_cultivo")

@login_required
def mover_arriba(request, pk):
    act = get_object_or_404(CultivoActividad, pk=pk)
    # Buscar la actividad anterior
    anterior = CultivoActividad.objects.filter(
        id_cultivo=act.id_cultivo, orden__lt=act.orden
    ).order_by('-orden').first()
    if anterior:
        # Intercambiar orden
        act.orden, anterior.orden = anterior.orden, act.orden
        act.save()
        anterior.save()
    return redirect('parametrizar_cultivo')

@login_required
def mover_abajo(request, pk):
    act = get_object_or_404(CultivoActividad, pk=pk)
    # Buscar la actividad siguiente
    siguiente = CultivoActividad.objects.filter(
        id_cultivo=act.id_cultivo, orden__gt=act.orden
    ).order_by('orden').first()
    if siguiente:
        # Intercambiar orden
        act.orden, siguiente.orden = siguiente.orden, act.orden
        act.save()
        siguiente.save()
    return redirect('parametrizar_cultivo')
