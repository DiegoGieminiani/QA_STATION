from django.db import models
from django.apps import apps
from django.utils.timezone import now

class TestCase(models.Model):
    test_case_id = models.AutoField(primary_key=True, verbose_name="ID del Caso de Prueba")
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Caso de Prueba")
    url = models.URLField(max_length=2048, verbose_name="URL del Caso de Prueba")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    resultado_esperado = models.TextField(verbose_name="Resultado Esperado") 
    functional_test_id = models.IntegerField(default=1, verbose_name="ID de la Prueba Funcional Asociada")  # Ajusta el valor predeterminado según tu lógica
    ...
    functional_test_id = models.IntegerField(verbose_name="ID de la Prueba Funcional Asociada")  # Usar apps.get_model

    def get_functional_test(self):
        FunctionalTest = apps.get_model("functional_tests", "FunctionalTest")
        return FunctionalTest.objects.filter(functional_test_id=self.functional_test_id).first()

    class Meta:
        verbose_name = "Caso de Prueba"
        verbose_name_plural = "Casos de Prueba"

    def __str__(self):
        return self.nombre

class StepByStep(models.Model):
    id_paso = models.AutoField(primary_key=True, verbose_name="ID del Paso")
    pasos = models.TextField(verbose_name="Descripción del Paso")
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name="steps", verbose_name="Caso de Prueba Asociado")
    orden = models.PositiveIntegerField(verbose_name="Orden del Paso")

    class Meta:
        verbose_name = "Paso a Paso"
        verbose_name_plural = "Pasos a Paso"

    def __str__(self):
        return f"Paso {self.orden} para el Caso {self.test_case.nombre}"
