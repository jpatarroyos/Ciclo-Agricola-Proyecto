from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Insumo, CompraInsumo, CicloActividadInsumo

from django.db.models import Sum
from django.utils.timezone import now
from django.contrib import messages
import datetime

@login_required
def gestionar_insumos(request):
    insumos = Insumo.objects.all()
    insumo_id = request.GET.get("insumo")  # insumo seleccionado en el combo
    compras = []
    actividades = []
    total_compras = 0
    total_utilizado = 0

    if insumo_id:
        compras = CompraInsumo.objects.filter(id_insumo=insumo_id)
        actividades = CicloActividadInsumo.objects.filter(id_insumo=insumo_id)
        total_compras = compras.aggregate(Sum("cantidad"))["cantidad__sum"] or 0
        total_utilizado = actividades.aggregate(Sum("cantidad_utilizada"))["cantidad_utilizada__sum"] or 0

    # Si se envía el formulario de compra
    if request.method == "POST":
        
        if "crear_compra" in request.POST:
            insumo_id = request.POST.get("insumo_id")
            fecha_compra = request.POST.get("fecha_compra") 
            marca = request.POST.get("marca")
            cantidad = request.POST.get("cantidad")

            # Validación: no permitir fechas futuras,(por si alguien manipula el limite del html)
            if fecha_compra > str(now().date()):
                messages.error(request, "La fecha no puede ser futura.")
                return redirect(f"/compra_insumos/?insumo={insumo_id}")
            
            CompraInsumo.objects.create(
                id_insumo_id=insumo_id,
                fecha_compra=fecha_compra,
                marca=marca,
                cantidad=cantidad,
                registrado_por=request.user
            )

            messages.success(request, "Compra registrada correctamente.")
            return redirect(f"/compra_insumos/?insumo={insumo_id}")

        if "editar_compra" in request.POST:
            compra_id = request.POST.get("compra_id")
            compra = CompraInsumo.objects.get(pk=compra_id)
            compra.marca = request.POST.get("marca")
            compra.cantidad = request.POST.get("cantidad")
            compra.save()
            return redirect(f"/compra_insumos/?insumo={compra.id_insumo.id_insumo}")
        
        # LÓGICA DE ELIMINACIÓN
        if "eliminar_compra" in request.POST:
            compra_id = request.POST.get("compra_id")
            compra = get_object_or_404(CompraInsumo, pk=compra_id)
            insumo = compra.id_insumo
            compra.delete()
            messages.success(request, "Registro de compra eliminado correctamente.")
            return redirect(f"/compra_insumos/?insumo={insumo.id_insumo}")

    
    return render(request, "compra_insumos.html", {
        "insumos": insumos,
        "compras": compras,
        "actividades": actividades,
        "total_compras": total_compras,
        "total_utilizado": total_utilizado,
        "insumo_id": insumo_id,
        "today" : datetime.date.today().strftime("%Y-%m-%d"),#le pasamos la fecha de hoy como limite
    })

    
