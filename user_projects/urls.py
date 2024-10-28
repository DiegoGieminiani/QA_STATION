from django.urls import path, include
from .views import project_view

urlpatterns = [
    path('',project_view, name='projects'),
]