from django.urls import path
from django.contrib.auth import views as auth_views
from app1.views.views import *
from app1.views.usuarios.views import *

urlpatterns = [
    path('iniciar_sesion/', iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('principal_miticket/', principal_miticket_view, name='principal_miticket'),

    # Vistas de Django de recuperar contraseña

    # Crear usuarios / consultar usuarios
    path('usuarios/perfil_de_usuario/<int:id>/', perfil_de_usuario_view, name='perfil_de_usuario'),

    # Consultar tickets

    # Vista de general reportes

    # -----

    # arreglar esta es para los reportes
    path('usuarios/list/', usuarios_list, name='usuarios_list'),

    #path('usuarios/list/', UsuariosListView.as_view(), name='usuarios_list')
]