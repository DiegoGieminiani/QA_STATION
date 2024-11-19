from django.db import models
from django.apps import apps
from django.utils.timezone import now
from user_projects.models import Project


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

class TestCase(models.Model):
    test_case_id = models.AutoField(primary_key=True, verbose_name="ID del Caso de Prueba")
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Caso de Prueba")
    url = models.URLField(max_length=2048, verbose_name="URL del Caso de Prueba")
    resultado_esperado = models.TextField(verbose_name="Resultado Esperado")  # Ajusta el valor predeterminado según tu lógica
    functional_test_id = models.OneToOneField(FunctionalTest, on_delete=models.CASCADE)  # Usar apps.get_model
    class Meta:
        verbose_name = "Caso de Prueba"
        verbose_name_plural = "Casos de Prueba"

    def __str__(self):
        return self.nombre

class StepByStep(models.Model):
    id_paso = models.AutoField(primary_key=True, verbose_name="ID del Paso")
    pasos = models.TextField(verbose_name="Descripción del Paso")
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name="steps", verbose_name="Caso de Prueba Asociado")

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
    paso_id = models.OneToOneField(
        StepByStep,
        on_delete=models.CASCADE, 
        verbose_name="ID del Paso Asociado")

    class Meta:
        verbose_name = "Acción"
        verbose_name_plural = "Acciones"

    def __str__(self):
        return self.action
