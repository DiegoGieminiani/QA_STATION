from django.contrib import admin
from .models import Project

# Registra el modelo Project en el admin
admin.site.register(Project)