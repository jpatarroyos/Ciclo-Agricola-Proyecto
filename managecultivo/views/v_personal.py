from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Personal
from django.http import JsonResponse
from django.contrib import messages

@login_required
def crear_personal(request):
    personas = Personal.objects.all()

    # Crear personal
    if request.method == "POST" and "crear_personal" in request.POST:
        id_cedula = request.POST.get("id_cedula")
        nombre = request.POST.get("nombre")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        rol = request.POST.get("rol")

        Personal.objects.create(
            id_cedula=id_cedula,
            nombre=nombre,
            telefono=telefono,
            email=email,
            rol=rol
        )
        messages.success(request, "Personal  creado correctamente.") #esto es para el panel admin de django
        return redirect("crear_personal")

    # Editar personal
    if request.method == "POST" and "editar_personal" in request.POST:
        persona_id = request.POST.get("persona_id")
        nombre = request.POST.get("nombre")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        rol = request.POST.get("rol")

        persona = get_object_or_404(Personal, pk=persona_id)
        persona.nombre = nombre
        persona.telefono = telefono
        persona.email = email
        persona.rol = rol
        persona.save()
        messages.success(request, "the personal "+ nombre + " was changed successfully.") 
        return redirect("crear_personal")
        
    return render(request, "crear_personal.html", {"personas": personas})

#Funcion para los modales
def persona_detalle(request, id):
    try:
        persona = Personal.objects.get(pk=id)
    except Personal.DoesNotExist:
        return JsonResponse({"error": "Persona no encontrada"}, status=404)

    data = {
        "persona": {
            "pk": persona.pk,
            "id_cedula": persona.id_cedula,
            "nombre": persona.nombre,
            "telefono": persona.telefono,
            "email": persona.email,
            "rol": persona.rol,
        }
    }
    return JsonResponse(data)

