from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID del Proyecto")  # Cambiado a 'id' para coincidir con la BD
    name = models.CharField(max_length=255, verbose_name="Nombre del Proyecto")
    description = models.TextField(verbose_name="Descripción del Proyecto")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects", verbose_name="Usuario")

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.name
