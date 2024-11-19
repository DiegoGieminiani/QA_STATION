from django.db import models
from django.apps import apps
from ai_module.models import Action, FunctionalTest


# Modelo de Result
class Result(models.Model):
    status = models.CharField(max_length=20, verbose_name="Estado")
    description = models.CharField(max_length=255, verbose_name="Descripción")
    evidence = models.CharField(max_length=255, blank=True, null=True, verbose_name="Evidencia")
    action = models.ForeignKey(
        Action,
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name="Acción Asociada"
    )

    class Meta:
        verbose_name = "Resultado"
        verbose_name_plural = "Resultados"

    def __str__(self):
        return f"{self.status} - Acción {self.action.action_id}"