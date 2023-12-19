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

    # Crear y Consultar tickets
    path('tickets/crear_ticket/', crear_ticket_view, name='crear_ticket'),
    path('tickets/consultar_ticket/', consultar_ticket_view, name='consultar_ticket'),
    path('eliminar_ticket/<int:id>/', eliminar_ticket, name='eliminar_ticket'),
    path('tickets/comentar_ticket/<int:id>/', comentar_ticket_view, name='comentar_ticket'),
    path('estado_prioridad_update/<int:id>/', estado_prioridad_update, name='estado_prioridad_update'),

    # Vista de Generar reportes
    path('reportes/generar_reportes/', reportes_view, name='generar_reportes'),
]