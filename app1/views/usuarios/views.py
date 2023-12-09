from django.shortcuts import render
from django.http import HttpResponse

from app1.models import *

# Create your views here.
def usuarios_list(request):
    data = {
        'title': 'Listado de usuarios',
        'usuarios': User.objects.all()
    }
    return render(request, 'usuarios/list.html', data)

# def testview(request):
#     return render(request, 'index.html', {
#         'name':'pepe',
#         'tickets': Ticket.objects.all()
#     })

# def testview2(request):
#     return render(request, 'test.html', {
#         'name':'pepe',
#         'usuarios': User.objects.all()
#     })