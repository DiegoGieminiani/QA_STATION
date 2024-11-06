# user_projects/forms.py
from django import forms
from .models import Project  # Importa el modelo Project desde models.py


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        labels = {
            'name': 'Nombre del Proyecto',
            'description': 'Descripción del Proyecto',
        }