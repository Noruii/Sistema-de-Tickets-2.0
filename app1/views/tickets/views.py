from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
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
                'icon': '<i class="fa-solid fa-ticket"></i>',
                'title': 'Crear un ticket',
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
            return redirect('consultar_ticket')
        except IntegrityError:
            messages.error(request, 'Error al crear el ticket.')
            return redirect('crear_ticket')

    return render(request, 'tickets/crear_ticket.html', {
        'icon': '<i class="fa-solid fa-ticket"></i>',
        'title': 'Crear un ticket',
        'departamentos': departamentos
    })

@login_required
def consultar_ticket_view(request):
    try:
        tickets = Ticket.objects.all()
        tickets_usuario_especifico = Ticket.objects.filter(usuario_id = request.user)
    except Ticket.DoesNotExist:
        raise Http404("El ticket no existe.")

    return render(request, 'tickets/consultar_ticket.html', {
        'icon': '<i class="fa-solid fa-user-edit"></i>',
        'title': 'Consultar tickets', 
        'tickets': tickets,
        'tickets_usuario_especifico': tickets_usuario_especifico,
    })

# En este código, primero se realiza la validación de campos obligatorios y se verifica que departamento sea un valor válido. 
# Si se encuentran errores, se envía un mensaje de error y se redirige de vuelta a la página de edición con el mismo id. 
# Si todo está bien, se actualizan los datos del ticket y se envía un mensaje de éxito.
@login_required
def editar_ticket_view(request, id):
    # definir la variable fuera del condicional para que este definida y accesible en ambos bloques de código.
    departamentos = Ticket.DEPARTAMENTO_CHOICES

    # listar los datos por id
    ticket = get_object_or_404(Ticket, id=id)

    if request.method == 'GET':
        # Verificar si el usuario es el creador del ticket o si es un administrador
        if request.user == ticket.usuario or request.user.is_staff or request.user.is_superuser:
            return render(request, 'tickets/editar_ticket.html', {
                'icon': '<i class="fa-solid fa-ticket"></i>',
                'title': 'Editar ticket',
                'ticket': ticket,
                'departamentos': departamentos
            })
        else:
            # Si el usuario no es el creador del ticket ni es un administrador, 
            # redirigir a una página de error o a una página que informe que no tiene permisos para acceder a ese ticket
            raise Http404('No tiene permisos para acceder a este ticket')
    else:
        # recibir los datos
        asunto = request.POST['txtAsunto']
        departamento = request.POST.get('formControlDepartamento')
        descripcion = request.POST['formControlDescripcion']

        # Validar campos obligatorios
        if not asunto or not descripcion:
            messages.error(request, 'Debe completar todos los campos obligatorios.')
            return redirect('editar_ticket', id=id)

        # Actualizar los datos
        ticket.asunto = asunto
        ticket.departamento = departamento
        ticket.descripcion = descripcion
        ticket.save()
        messages.success(request, '¡Ticket editado exitosamente!')
        return redirect('consultar_ticket')

@login_required
def eliminar_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    print(ticket)
    # ticket.delete()
    messages.success(request, f'¡Ticket #{ticket.id} eliminado exitosamente!')
    return redirect('consultar_ticket')

@login_required
def comentar_ticket_view(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    comentarios = Comentario.objects.filter(FK_id_ticket=ticket)
    estados = Estado.ESTADO_CHOICES
    prioridades = Prioridad.PRIORIDAD_CHOICES

    # Obtener el estado y prioridad actual para mostrarlo en el HTML
    try:
        estado_actual = Estado.objects.filter(FK_id_ticket=ticket).order_by('-fecha_modificacion').first()
        prioridad_actual = Prioridad.objects.filter(FK_id_ticket=ticket).order_by('-fecha_modificacion').first()

        # Para cambiar estado a 'En progreso' cuando se comenta
        estado_actual_update = Estado.objects.get(FK_id_ticket=ticket)

    except Estado.DoesNotExist or Prioridad.DoesNotExist:
        estado_actual = None
        prioridad_actual = None

    # Verificar si el usuario es el creador del ticket o si es un administrador
    if request.user == ticket.usuario or request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            # Verificar que los campos obligatorios estén completos
            if not request.POST.get('textAreacomentario'):
                messages.error(request, 'Por favor, complete todos los campos obligatorios.')  
                return redirect('comentar_ticket', id=id)
            try:
                comentario_texto = request.POST['textAreacomentario']
                usuario = request.user
                comentario = Comentario.objects.create(
                    comentario=comentario_texto,
                    usuario=usuario,
                    FK_id_ticket=ticket 
                )
                comentario.save()
                ticket.asignado_a = usuario
                ticket.save()
                # Pasar estado del ticket a 'En progreso' al añadir un comentario
                if estado_actual_update.estado == 'Abierto':
                    estado_actual = estados[1][0]
                    estado_actual_update.estado = estado_actual
                    estado_actual_update.save()

                messages.success(request, '¡Comentario agregado correctamente!')
                return redirect('comentar_ticket', id=id)
            except IntegrityError:
                messages.error(request, 'Error al comentar el ticket.')
                return redirect('comentar_ticket', id=id)

        return render(request, 'tickets/comentar_ticket.html', {
            'icon': '<i class="fa-solid fa-comments"></i>',
            'title': 'Comentar ticket',
            'ticket': ticket,
            'comentarios': comentarios,
            'estados': estados,
            'estado_actual': estado_actual,
            'prioridades': prioridades,
            'prioridad_actual': prioridad_actual
        })
    else:
        # Si el usuario no es el creador del ticket ni es un administrador, 
        # redirigir a una página de error o a una página que informe que no tiene permisos para acceder a ese ticket
        raise Http404('No tiene permisos para acceder a este ticket')

@login_required
def estado_prioridad_updated(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    estado = Estado.objects.get(FK_id_ticket=ticket)
    prioridad = Prioridad.objects.get(FK_id_ticket=ticket)

    if request.method == 'POST':
        try:
            usuario = request.user

            estado_updated = request.POST['estado']
            estado.estado = estado_updated
            estado.usuario_modificacion = usuario
            estado.save()

            prioridad_updated = request.POST['prioridad']
            prioridad.prioridad = prioridad_updated
            prioridad.usuario_modificacion = usuario
            prioridad.save()

            messages.success(request, '¡Estado y prioridad cambiados exitosamente!')
            messages.success(request, f'¡El estado y la prioridad del ticket an pasado a {estado_updated} y {prioridad_updated}!')  
            return redirect('comentar_ticket', id=id)
        except:
            messages.error(request, 'Error al cambiar el estado y la prioridad.')  
            return redirect('comentar_ticket', id=id)
    return redirect('comentar_ticket', id=id)