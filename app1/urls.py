from django.urls import path
from django.contrib.auth import views as auth_views
from app1.views.usuarios.views import *

urlpatterns = [
    # path('uno/', views.testview, name='view1'),
    # path('dos/', views.testview2, name='view2'),

    path('usuarios/list/', usuarios_list, name='usuarios_list')
    #path('usuarios/list/', UsuariosListView.as_view(), name='usuarios_list')
]