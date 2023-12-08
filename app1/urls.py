from django.urls import path
from app1 import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('uno/', views.testview, name='view1'),
    path('dos/', views.testview2, name='view2'),
    
]