from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from app1.models import *

# Create your views here.

# Vistas basada en funcion
def usuarios_list(request):
    data = {
        'title': 'Listado de usuarios',
        'usuarios': User.objects.all()
    }
    return render(request, 'usuarios/list.html', data)

# buena explicacion https://youtu.be/iP4LxWbbpy8?si=A5hF7fx466GCTfD3
# ListView | Vistas basadas en clases (manda 'object_list' a la plantilla html revisar doc django)
class UsuariosListView(ListView):
    model = User
    template_name = "usuarios/list.html"

    # sobrescreebir este metodo que devuelve el diccionario que representa el contexto de la platilla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de usuarios'
        # context['object_list'] = Ticket.objects.allK() # puedes sobreescribir el atributo 'object_list' para que en vez del modelo 'User' mande otro modelo
        return context
    
