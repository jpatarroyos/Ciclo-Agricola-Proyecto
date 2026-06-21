from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import Group, User

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
        return redirect("crear_usuario")

    return render(request, "crear_usuario.html", {"usuarios": usuarios})
