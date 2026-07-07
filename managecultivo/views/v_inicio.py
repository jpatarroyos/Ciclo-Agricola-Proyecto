from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login as auth_login
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from ..models import CicloActividad

import datetime

def home(request):
    return render(request, "home.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("bienvenida")
        else:
            return render(request, "login.html", {"error": "Usuario o contraseña incorrectos"})
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def bienvenida(request):
    fecha_hoy = timezone.localdate()  # 🔹 solo la fecha
    actividades_hoy = (
        CicloActividad.objects
        .filter(fecha_programada=fecha_hoy)
        .select_related("id_ciclo", "id_actividad", "id_ciclo__id_cultivo", "id_ciclo__id_zonaagricola")
        .order_by("-id_actividad__prioridad")  # Alta primero
    )
    context = {
        "usuario": request.user,
        "fecha_hoy": fecha_hoy,
        "actividades_hoy": actividades_hoy,
    }
    return render(request, "bienvenida.html", context)