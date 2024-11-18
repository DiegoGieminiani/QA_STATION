from django.db import models
from django.apps import apps
from user_projects.models import Project

# Modelo de FunctionalTest
class FunctionalTest(models.Model):
    functional_test_id = models.AutoField(primary_key=True, verbose_name="ID de la Prueba Funcional")
    url = models.URLField(max_length=2048, verbose_name="URL de la Prueba Funcional")
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="functional_tests",
        verbose_name="Proyecto Asociado"
    )

    class Meta:
        verbose_name = "Prueba Funcional"
        verbose_name_plural = "Pruebas Funcionales"

    def __str__(self):
        return f"Prueba Funcional {self.functional_test_id}"


# Modelo de Action
class Action(models.Model):
    action_id = models.AutoField(primary_key=True, verbose_name="ID de la Acción")
    action = models.CharField(max_length=255, verbose_name="Acción")
    element_type = models.CharField(max_length=100, verbose_name="Tipo de Elemento")
    value = models.CharField(max_length=255, blank=True, null=True, verbose_name="Valor")
    input_value = models.CharField(max_length=255, blank=True, null=True, verbose_name="Valor de Entrada")
    functional_test = models.ForeignKey(
        FunctionalTest,
        on_delete=models.CASCADE,
        related_name="actions",
        verbose_name="Prueba Funcional"
    )
    paso_id = models.IntegerField(null=True, blank=True, verbose_name="ID del Paso Asociado")

    def get_paso(self):
        StepByStep = apps.get_model("ai_module", "StepByStep")
        return StepByStep.objects.filter(id=self.paso_id).first()

    class Meta:
        verbose_name = "Acción"
        verbose_name_plural = "Acciones"

    def __str__(self):
        return self.action


# Modelo de Result
class Result(models.Model):
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
        ('PENDING', 'Pending'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Estado")
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
