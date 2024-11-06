from django.urls import path
from . import views

app_name = 'user_projects'

urlpatterns = [
    path('', views.project_view, name='projects'),
    path('select/<int:project_id>/', views.select_project, name='select_project'),
    path('delete/<int:project_id>/', views.delete_project, name='delete_project'),
]
