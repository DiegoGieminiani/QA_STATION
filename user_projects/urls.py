# user_projects/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_view, name='projects'),

     # Ruta para agregar proyecto
]