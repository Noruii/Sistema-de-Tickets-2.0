from typing import Any
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from app1.models import *

# Create your views here.

@login_required
def perfil_de_usuario_view(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == 'GET':
        # Verificar si el usuario esta entrando a su propio perfil
        if request.user.id == usuario.id:
            return render(request, 'usuarios/perfil_de_usuario.html', {
                'usuario': usuario
            })
        else:
            raise Http404('No tiene permisos para acceder a este perfil')