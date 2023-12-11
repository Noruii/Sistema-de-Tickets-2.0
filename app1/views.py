from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from django.contrib import messages

from app1.models import *

# Create your views here.

# Vistas basada en funcion
def usuarios_list(request):
    data = {
        'title': 'Listado de usuarios',
        'usuarios': User.objects.all()
    }
    return render(request, 'usuarios/list.html', data)

def iniciar_sesion(request):
    return render(request, 'registro/login.html')
    # if request.method == 'GET':
    #     return render(request, 'loginticket.html')
    # else:
    #     user = authenticate(request, 
    #         username=request.POST['user_nombre'],
    #         password=request.POST['user_clave1']
    #     )
    #     # Comprobando si el usuario es normal o admin 
    #     # TODO: arreglar...
    #     if user is None:
    #         messages.error(request, 'El usuario o la contraseña son incorrectos.')
    #         return redirect('iniciar_sesion') 
    #     else:
    #         login(request, user)
    #         if request.user.is_superuser or request.user.is_staff:
    #             return redirect('principal_miticket')
    #         else:
    #             return redirect('principal_miticket') 

#@login_required
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
    
