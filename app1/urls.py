from django.urls import path
from django.contrib.auth import views as auth_views
from app1.views import *

urlpatterns = [
    # path('uno/', views.testview, name='view1'),
    # path('dos/', views.testview2, name='view2'),

    path('iniciar_sesion/', iniciar_sesion, name='iniciar_sesion'),
    path('principal_miticket/', principal_miticket_view, name='principal_miticket'),

    # arreglar esta es para los reportes
    path('usuarios/list/', usuarios_list, name='usuarios_list'),

    #path('usuarios/list/', UsuariosListView.as_view(), name='usuarios_list')
]