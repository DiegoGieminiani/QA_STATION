from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_view, name='projects'),
    path('select/', views.select_project, name='select_project'),

]