from typing import Any
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

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
    else:
        if 'editar_perfil' in request.POST:
            # procesar el formulario del modal de editar perfil
            # recibir los datos
            print(request.POST)
            print(request.FILES)
            nombre = request.POST.get('first_name')
            apellido = request.POST.get('last_name')
            email = request.POST.get('email')
            imagenPerfil = request.FILES.get('imagenPerfil')

            # validar que la img de perfil no este vacia
            if imagenPerfil is not None:
                usuario.first_name = nombre
                usuario.last_name = apellido
                usuario.email = email
                usuario.avatar = imagenPerfil
                usuario.save()
                messages.success(request, f'¡Imagen de perfil actualizada exitosamente!')
                return redirect('perfil_de_usuario', id=id)

            # Validar si no se cambiaron datos y se presiono el boton de guardar
            if (request.POST.get('first_name') == usuario.first_name and
                request.POST.get('last_name') == usuario.last_name and
                request.POST.get('email') == usuario.email):
                return redirect('perfil_de_usuario', id=id)

            # Validar campos obligatorios
            if not nombre or not apellido or not email:
                messages.error(request, 'Debe completar todos los campos obligatorios.')
                return redirect('perfil_de_usuario', id=id)
            
            # validar correo
            # validate_email solo verifica si el correo es valido no verifica si a ese correo es 'real' o enviable
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Ingrese un correo electrónico válido.')
                return redirect('perfil_de_usuario', id=id)

            # actualizar los datos
            usuario.first_name = nombre
            usuario.last_name = apellido
            usuario.email = email
            usuario.save()
            messages.success(request, f'¡Perfil actualizado exitosamente!')
            return redirect('perfil_de_usuario', id=id)
        else:
            messages.error(request, f'No se pudiron editar los datos.')
            return redirect('perfil_de_usuario', id=id)

def gestion_de_usuarios_view(request):
    data = {
        'icon': '<i class="fa-solid fa-users"></i>',
        'title': 'Gestion de usuarios',
        'usuarios': User.objects.all()
    }
    return render(request, 'usuarios/gestion_de_usuarios.html', data)