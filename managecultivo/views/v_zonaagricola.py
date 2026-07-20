from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import ZonaAgricola
from django.contrib import messages

@login_required
def crear_zonaagricola(request):
    zonas = ZonaAgricola.objects.all()

    # Crear zona
    if request.method == "POST" and "crear_zonaagricola" in request.POST: #mira el nombre del boton
        nombre = request.POST.get("nombre")
        ubicacion = request.POST.get("ubicacion")
        direccion = request.POST.get("direccion")

        ZonaAgricola.objects.create(
            nombre=nombre,
            ubicacion=ubicacion,
            direccion=direccion,
            registrado_por=request.user
        )
        return redirect("crear_zonaagricola")

    # Editar zona
    if request.method == "POST" and "editar_zonaagricola" in request.POST:
        zona_id = request.POST.get("zona_id")
        nombre = request.POST.get("nombre")
        ubicacion = request.POST.get("ubicacion")
        direccion = request.POST.get("direccion")

        zona = get_object_or_404(ZonaAgricola, pk=zona_id)
        zona.nombre = nombre
        zona.ubicacion = ubicacion
        zona.direccion = direccion
        zona.save()
        return redirect("crear_zonaagricola")
    
    # LÓGICA DE ELIMINACIÓN.(falta mejorarla)
    if request.method == "POST" and "eliminar_zona" in request.POST:
        zona_id = request.POST.get("zona_id")
        zona = get_object_or_404(ZonaAgricola, pk=zona_id)
        #comprobar que no hayan ciclos
        if zona.fk_ciclo2.exists():
            # Si existen ciclos, enviamos un mensaje de error y detenemos el borrado
            messages.error(request, f"No se puede eliminar la zona '{zona.nombre}' porque tiene ciclos agrícolas asociados.")
        else:
            # Si está limpio, se borra con éxito
            zona.delete()
            messages.success(request, "Zona Agrícola eliminada correctamente.")

        return redirect("crear_zonaagricola")
        

    return render(request, "crear_zonaagricola.html", {"zonas": zonas})
