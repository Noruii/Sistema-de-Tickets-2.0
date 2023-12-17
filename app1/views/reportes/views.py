from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from app1.models import *

# Create your views here.

@login_required
def reportes_view(request):
    data = {
        'icon': '<i class="fa-solid fa-file-lines"></i>',
        'title': 'Generar reportes',        
        'tickets': Ticket.objects.all()
    }
    return render(request, 'reportes/generar_reportes.html', data)