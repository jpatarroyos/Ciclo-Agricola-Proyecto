from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import ZonaAgricola

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

    return render(request, "crear_zonaagricola.html", {"zonas": zonas})
