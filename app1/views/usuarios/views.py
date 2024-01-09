import json
from django.db import IntegrityError
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail
from app1.models import *

# Create your views here.
def validar_requisitos_contrasena(password):
    if len(password) < 8:
        raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
    if not any(char.isdigit() for char in password):
        raise ValidationError('La contraseña debe contener al menos un número.')
    if not any(char.isupper() for char in password):
        raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
    if not any(char.islower() for char in password):
        raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
    if not any(char in ['$', '#', '@'] for char in password):
        raise ValidationError('La contraseña debe contener al menos uno de los siguientes caracteres especiales: $ # @.')

@login_required
def perfil_de_usuario_view(request, id):
    usuario = get_object_or_404(User, id=id)
    password1 = request.POST.get('password1', '')
    password2 = request.POST.get('password2', '')
    password3 = request.POST.get('passwordModal', '')
    print(password1, password2, password3)
    data = {
        'icon': '<i class="fa-solid fa-user"></i>',
        "title": 'Editar perfil',
        'usuario': usuario,
        'password1': password1,
        'password2': password2,
        'password3': password3
    }
    if 'editar_perfil' in request.POST:
        # procesar el formulario del modal de editar perfil
        # recibir los datos
        print(f'POST: {request.POST}')
        print(f'FILES: {request.FILES}')
        nombre = request.POST.get('first_name')
        apellido = request.POST.get('last_name')
        email = request.POST.get('email')
        imagenPerfil = request.FILES.get('imagenPerfil')

        # validar que la imagen de perfil no este vacia
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

        # Actualizar los datos
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = email
        usuario.save()

        # Actualizar datos en el tickets
        tickets_usuario_especifico = Ticket.objects.filter(usuario_id = usuario)
        for ticket in tickets_usuario_especifico:
            ticket.usuario.first_name = nombre
            ticket.usuario.last_name = apellido
            ticket.email = email
            ticket.save()

        messages.success(request, f'¡Perfil actualizado exitosamente!')
        return redirect('perfil_de_usuario', id=id)
    elif 'cambiar_contrasena' in request.POST:
        # procesar el formulario de cambiar contraseña 
        # Validar campos obligatorios
        if not password1 or not password2 or not password3:
            messages.error(request, 'Debe completar todos los campos obligatorios.')
            return render(request, 'usuarios/perfil_de_usuario.html', data)
        
        # Validar que la contraseña cumple los requisitos
        try:
            validar_requisitos_contrasena(password2)
        except ValidationError as error:
            error_message = getattr(error, 'message', None)
            messages.error(request, error_message)
            return render(request, 'usuarios/perfil_de_usuario.html', data)
        
        # validar que la contraseña actual sea correcta
        if request.user.check_password(password1):
            # validar contraseñas nuevas
            if password2 != password3:
                messages.error(request, 'Las contraseñas nuevas no coinciden.')
                return render(request, 'usuarios/perfil_de_usuario.html', data)
            
            # actualizar contraseña del usuario
            # usuario.set_password(password2)
            # usuario.save()
            # volver a autenticar al usuario con la nueva contraseña
            user = authenticate(username=usuario.username, password=password2)
            if user is not None:
                login(request, user)

            # Mandar un correo
            subject = 'Cambio de contraseña'
            message = 'Se a realizado un cambio de contraseña en su cuenta del sistema de tickets.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [usuario.email]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            messages.success(request, f'¡Contraseña cambiada exitosamente!')
            return redirect('perfil_de_usuario', id=id)
        else:
            messages.error(request, f'La contraseña actual es incorrecta.')
            return render(request, 'usuarios/perfil_de_usuario.html', data)
    
    # Verificar si el usuario esta entrando a su propio perfil
    if request.user.id == usuario.id:
        return render(request, 'usuarios/perfil_de_usuario.html', data)
    else:
        raise Http404('No tiene permisos para acceder a este perfil.')

@login_required
def gestion_de_usuarios_view(request):
    if request.user.is_superuser or request.user.is_staff:
        data = {
        'icon': '<i class="fa-solid fa-users"></i>',
        'title': 'Gestion de usuarios',
        'usuarios': User.objects.all() #.exclude(id=request.user.id)
        }
        return render(request, 'usuarios/gestion_de_usuarios.html', data)
    return redirect('principal_miticket')

@login_required
def crear_usuario_view(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            # Obtener los datos del formulario
            matricula = request.POST['matricula']
            nombre = request.POST['first_name']
            apellido = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            print(matricula, nombre, apellido, email, password1, password2)

            data = {
                'icon': '<i class="fa-solid fa-user"></i>',
                'title': 'Crear un usuario',
                'matricula': matricula,
                'nombre': nombre,
                'apellido': apellido,
                'email': email,
                'password1': password1,
                'password2': password2
            }

            # Verificar que los campos obligatorios estén completos
            if not matricula or not nombre or not apellido or not email or not password1 or not password2:
                messages.error(request, 'Por favor, complete todos los campos obligatorios.')
                return render(request, 'usuarios/crear_usuario.html', data)
            
            # validar correo
            # validate_email solo verifica si el correo es valido no verifica si a ese correo es 'real' o enviable
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Ingrese un correo electrónico válido.')
                return render(request, 'usuarios/crear_usuario.html', data)
            
            # Validar que la contraseña cumple los requisitos
            try:
                validar_requisitos_contrasena(password1)
            except ValidationError as error:
                error_message = getattr(error, 'message', None)
                messages.error(request, error_message)
                return render(request, 'usuarios/crear_usuario.html', data)

            if request.user.check_password(request.POST['passwordModal']):
                if request.POST['password1'] == request.POST['password2']:
                    try:
                        rol_de_usuario = request.POST.get('flexRadioRol')

                        # Crear el nuevo usuario
                        user_args = {
                            'username': matricula, # Arreglar: el username sigue siendo requerido por alguna razon...
                            'matricula': matricula,
                            'first_name': nombre,
                            'last_name': apellido,
                            'email': email,
                            'password': password1,
                        }

                        if rol_de_usuario == 'Staff':
                            user_args['is_staff'] = True
                        elif rol_de_usuario == 'SuperUser':
                            user_args['is_superuser'] = True

                        # Se pasa el diccionario al método create_user() utilizando la sintaxis de desempaquetado **
                        user = User.objects.create_user(**user_args)
                        user.save()
                        
                        messages.success(request, f'Usuario ``{user.matricula}: {user.first_name} {user.last_name}`` creado exitosamente')
                        return redirect('gestion_de_usuarios')
                    except IntegrityError as error:
                        print(error)
                        messages.error(request, 'El usuario que intenta crear ya existe.')
                        return render(request, 'usuarios/crear_usuario.html', data)
                else:
                    messages.error(request, 'Las contraseñas del usuario no coinciden.')
                    return render(request, 'usuarios/crear_usuario.html', data)
            else:
                messages.error(request, 'Contraseña de confirmación incorrecta.')
                return render(request, 'usuarios/crear_usuario.html', data)

        # Mostrar el formulario para crear un nuevo usuario
        return render(request, 'usuarios/crear_usuario.html', {
            'icon': '<i class="fa-solid fa-user"></i>',
            'title': 'Crear un usuario'
        })
    return redirect('gestion_de_usuarios')

@login_required
def editar_usuario_view(request, id):
    if request.user.is_superuser or request.user.is_staff:
        usuario = get_object_or_404(User, id=id)

        if request.method == 'POST':
            # Obtener los datos del formulario
            nombre = request.POST['first_name']
            apellido = request.POST['last_name']
            email = request.POST['email']
            rol_de_usuario = request.POST.get('flexRadioRol')

            # Validar campos obligatorios estan llenos
            if not nombre or not apellido or not email:
                messages.error(request, 'Debe completar todos los campos obligatorios.')
                return redirect('editar_usuario', id=id)
            
            # validar correo
            # validate_email solo verifica si el correo es valido no verifica si a ese correo es 'real' o enviable
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Ingrese un correo electrónico válido.')
                return redirect('editar_usuario', id=id)

            if request.user.check_password(request.POST['passwordModal']):
                try:
                    # actualizar los datos
                    staff = False
                    superuser = False

                    if rol_de_usuario == 'Staff':
                        staff = True
                    elif rol_de_usuario == 'SuperUser':
                        staff = True
                        superuser = True

                    usuario.first_name = nombre
                    usuario.last_name = apellido
                    usuario.email = email
                    usuario.is_staff = staff
                    usuario.is_superuser = superuser
                    usuario.save()

                    messages.success(request, f'¡Usuario ``{usuario.matricula}: {usuario.first_name} {usuario.last_name}`` editado exitosamente!')
                    return redirect('gestion_de_usuarios')
                except IntegrityError:
                    messages.error(request, 'Error al editar el usuario.')
                    return redirect('gestion_de_usuarios')
            else:
                messages.error(request, 'Contraseña de confirmación incorrecta. Vuelva a intentarlo.')
                return redirect('editar_usuario', id)

        return render(request, 'usuarios/editar_usuario.html', {
            'icon': '<i class="fa-solid fa-user"></i>',
            'title': 'Editar usuario',
            'usuario': usuario
        })
    else:
        raise Http404('No tiene permisos para acceder a esta pagina')

@login_required
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    # usuario.delete()
    messages.success(request, f'¡Usuario ``{usuario.matricula}: {usuario.first_name} {usuario.last_name}`` eliminado exitosamente!')
    return redirect('gestion_de_usuarios')

@login_required
def validar_contrasena_eliminar(request):
    if request.method == 'POST':
        # Analizar el cuerpo de la solicitud y obtener los datos JSON
        data = json.loads(request.body)
        print('data: ', data)
        password = data.get('password')        
        if password and request.user.check_password(password):
            return JsonResponse({'valid': True})
    return JsonResponse({'valid': False})