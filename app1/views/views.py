from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib import messages

from app1.models import *

# Create your views here.

# Vistas basadas en funcion

def iniciar_sesion(request):
    if request.method == 'POST':
        p = request.POST
        print(p)
        matricula = request.POST.get('matricula')
        password = request.POST.get('password')
        user = authenticate(request, matricula=matricula, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('principal_miticket')

        messages.error(request, 'La matrícula o la contraseña son incorrectas.')
    
    return render(request, 'registro/login.html') 

@login_required
def cerrar_sesion(request):
    # TODO: 
    # Ingeniate como hacer esto... con el sweetalerts
    # messages.warning(request, '¿Seguro que quiere cerrar sesión?')
    logout(request)
    return redirect('iniciar_sesion')

@login_required
def principal_miticket_view(request):
    return render(request, 'principal_miticket.html')





# buena explicacion https://youtu.be/iP4LxWbbpy8?si=A5hF7fx466GCTfD3
# ListView | Vistas basadas en clases (manda 'object_list' a la plantilla html revisar doc django)
# class UsuariosListView(ListView):
#     model = User
#     template_name = "usuarios/list.html"

#     # sobrescreebir este metodo que devuelve el diccionario que representa el contexto de la platilla
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Listado de usuarios'
#         # context['object_list'] = Ticket.objects.allK() # puedes sobreescribir el atributo 'object_list' para que en vez del modelo 'User' mande otro modelo
#         return context