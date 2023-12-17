from typing import Any
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib import messages

from app1.models import *

@login_required
def crear_ticket_view(request):
    departamentos = Ticket.DEPARTAMENTO_CHOICES

    if request.method == 'POST':

        asunto = request.POST['txtAsunto']
        selected_departamento = request.POST.get('formControlDepartamento', False)
        descripcion = request.POST['formControlDescripcion']
        # Usuario logeado
        usuario = request.user

        # Verificar que los campos obligatorios estén completos
        # Con y sin comprensión de listas.
        # if not all(field in request.POST and request.POST[field] for field in ['txtAsunto', 'formControlDepartamento', 'formControlDescripcion']):
        if not request.POST.get('txtAsunto') or not request.POST.get('formControlDepartamento') or not request.POST.get('formControlDescripcion'):
            messages.error(request, 'Por favor, complete todos los campos obligatorios.')
            return render(request, 'tickets/crear_ticket.html', {
                'asunto': asunto,
                'departamentos': departamentos,
                'selected_departamento': selected_departamento,
                'descripcion': descripcion
            })

        try:
            ticket = Ticket.objects.create(
                asunto=asunto,
                departamento=selected_departamento,
                descripcion=descripcion,
                usuario=usuario
            )
            ticket.save()

            estados = Estado.ESTADO_CHOICES
            estado = Estado.objects.create(
                FK_id_ticket=ticket,
                usuario_creacion=usuario,
                usuario_modificacion=usuario,
                estado=estados[0][0]
            )
            estado.save()

            prioridades = Prioridad.PRIORIDAD_CHOICES
            prioridad = Prioridad.objects.create(
                FK_id_ticket=ticket,
                usuario_creacion=usuario,
                usuario_modificacion=usuario,
                prioridad=prioridades[0][0]
            )
            prioridad.save()

            messages.success(request, '¡Ticket creado exitosamente!')
            return redirect('crear_ticket')
        except IntegrityError:
            messages.error(request, 'Error al crear el ticket.')
            return redirect('crear_ticket')

    return render(request, 'tickets/crear_ticket.html', {
        'departamentos': departamentos
    })
