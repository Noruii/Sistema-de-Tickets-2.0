from django.urls import path
from django.contrib.auth import views as auth_views
from app1.views.views import *
from app1.views.usuarios.views import *
from app1.views.reportes.views import *
from app1.views.tickets.views import *

urlpatterns = [
    path('iniciar_sesion/', iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('principal_miticket/', principal_miticket_view, name='principal_miticket'),

    # Vistas de Django de recuperar contraseña

    # Crear usuarios / Gestionar usuarios
    path('usuarios/perfil_de_usuario/<int:id>/', perfil_de_usuario_view, name='perfil_de_usuario'),
    path('usuarios/gestion_de_usuarios', gestion_de_usuarios_view, name="gestion_de_usuarios"),
    path('usuarios/crear_usuario/', crear_usuario_view, name='crear_usuario'),
    path('usuarios/editar_usuario/<int:id>/', editar_usuario_view, name='editar_usuario'),
    path('eliminar_usuario/<int:id>/', eliminar_usuario, name='eliminar_usuario'),
    path('validar_contrasena/', validar_contrasena_eliminar, name='validar_contrasena'),

    # Crear y Consultar tickets
    path('tickets/crear_ticket/', crear_ticket_view, name='crear_ticket'),
    path('tickets/consultar_ticket/', consultar_ticket_view, name='consultar_ticket'),
    path('tickets/editar_ticket/<int:id>/', editar_ticket_view, name='editar_ticket'),
    path('eliminar_ticket/<int:id>/', eliminar_ticket, name='eliminar_ticket'),
    path('tickets/comentar_ticket/<int:id>/', comentar_ticket_view, name='comentar_ticket'),
    path('estado_prioridad_updated/<int:id>/', estado_prioridad_updated, name='estado_prioridad_updated'),

    # Vista de Generar reportes
    path('reportes/generar_reportes/', reportes_view, name='generar_reportes'),
]