from django.urls import path
from app1.views.usuarios.views import usuarios_list
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('uno/', views.testview, name='view1'),
    # path('dos/', views.testview2, name='view2'),
    path('usuarios/list/', usuarios_list, )
]