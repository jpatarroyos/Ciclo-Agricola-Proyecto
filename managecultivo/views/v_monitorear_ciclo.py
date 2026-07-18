from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from ..models import CicloMonitoreo, Ciclo


@login_required
def ciclo_monitoreo(request):
    fecha_hoy = timezone.localdate()

    # lista de ciclos para el combo
    ciclos = Ciclo.objects.select_related("id_cultivo", "id_zonaagricola").all()

    ciclo_id = request.GET.get("ciclo")  # ciclo seleccionado
    monitoreos = CicloMonitoreo.objects.none()

    if ciclo_id:
        monitoreos = CicloMonitoreo.objects.filter(id_ciclo_id=ciclo_id)

    # creación de monitoreo
    if request.method == "POST" and "crear_monitoreo" in request.POST:
        observacion = request.POST.get("observacion")
        ciclo_id = request.POST.get("ciclo_id")

        if ciclo_id:
            CicloMonitoreo.objects.create(
                id_ciclo_id=ciclo_id,
                fecha=fecha_hoy,
                observacion=observacion,
                registrado_por=request.user
            )
        return redirect("monitorear_ciclo")

    context = {
        "fecha_hoy": fecha_hoy,
        "ciclos": ciclos,
        "monitoreos": monitoreos,
        "ciclo_id": ciclo_id,
    }
    return render(request, "monitorear_ciclo.html", context)

