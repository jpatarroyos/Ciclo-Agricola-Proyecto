from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Ciclo
@login_required
def calendario_ciclo(request):
    context = {
        "ciclos": Ciclo.objects.all()
    }
    return render(request, 'calendario_ciclo.html', context)