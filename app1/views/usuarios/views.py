from django.db import IntegrityError
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
                'icon': '<i class="fa-solid fa-user"></i>',
                "title": 'Editar perfil',
                'usuario': usuario
            })
        else:
            raise Http404('No tiene permisos para acceder a este perfil.')
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
            if len(password1) < 8:
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
                return render(request, 'usuarios/crear_usuario.html', data)
            if not any(char.isdigit() for char in password1):
                messages.error(request,'La contraseña debe contener al menos un número.')
                return render(request, 'usuarios/crear_usuario.html', data)
            if not any(char.isupper() for char in password1):
                messages.error(request,'La contraseña debe contener al menos una letra mayúscula.')
                return render(request, 'usuarios/crear_usuario.html', data)
            if not any(char.islower() for char in password1):
                messages.error(request,'La contraseña debe contener al menos una letra minúscula.')
                return render(request, 'usuarios/crear_usuario.html', data)
            if not any(char in ['$', '#', '@'] for char in password1):
                messages.error(request,'La contraseña debe contener al menos uno de los siguientes caracteres especiales: $ # @.')
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
                        
                        messages.success(request, f'Usuario ``{user.first_name} - {user.last_name}`` creado exitosamente')
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