# user_projects/forms.py
from django import forms
from .models import Project  # Importa el modelo Project desde models.py

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project  # Aquí usas el modelo Project definido en models.py
        fields = ['name', 'description']  # Incluye los campos que deseas en el formulario
