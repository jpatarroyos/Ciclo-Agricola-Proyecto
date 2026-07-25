from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import Group, User
from django.http import JsonResponse
from django.contrib import messages

#Crea o edita Usuarios
@login_required
def crear_usuario(request):
    usuarios = User.objects.all()

    # Crear usuario
    if request.method == "POST" and "crear_usuario" in request.POST:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        group_name = request.POST.get("group")

        # Crear usuario
        user = User.objects.create_user(username=username, email=email, password=password)

        # Asignar grupo
        if group_name:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

        messages.success(request, "Usuario creado correctamente.") #esto es para el panel admin de django

        return redirect("crear_usuario")

    # Editar usuario
    if request.method == "POST" and "editar_usuario" in request.POST:
        usuario_id = request.POST.get("usuario_id")
        email = request.POST.get("email")
        group_name = request.POST.get("group")

        user = get_object_or_404(User, id=usuario_id)

        # Actualizar email
        user.email = email

        # Actualizar grupo
        if group_name:
            group = Group.objects.get(name=group_name)
            user.groups.clear()
            user.groups.add(group)

        user.save()
        messages.success(request, "Usuario "+ user.username + " was changed successfully.")         
        return redirect("crear_usuario")

    return render(request, "crear_usuario.html", {"usuarios": usuarios})

#Funcion para los modales

def usuario_detalle(request, id):
    try:
        usuario = User.objects.get(pk=id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    # Obtenemos de forma segura el nombre del primer grupo si existe
    primer_grupo = usuario.groups.first()
    nombre_grupo = primer_grupo.name if primer_grupo else "Sin grupo"

    data = {
        "usuario": {  # Cambiado de "zona" a "usuario" para coincidir con JS
            "pk": usuario.pk,
            "nombre": usuario.username, # Coincide con data.usuario.nombre
            "email": usuario.email,     # Coincide con data.usuario.email
            "group": nombre_grupo,      # Cambiado de "group_name" a "group"
        }
    }
    return JsonResponse(data)

