from django.shortcuts import render
from django.http import HttpResponse

from .models import Usuarios, Ticket, Comentario, Estado, Prioridad

# Create your views here.
def testview(request):
    return render(request, 'home.html', {
        'name':'pepe',
        'tickets': Ticket.objects.all()
    })

def testview2(request):
    return render(request, 'index.html', {
        'name':'pepe',
        'usuarios': Usuarios.objects.all()
    })