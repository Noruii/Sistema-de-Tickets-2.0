from django.urls import path
from app1 import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('testview/', views.testview, name='testview'),
]