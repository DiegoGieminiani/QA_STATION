from django.db import models
from user_projects.models import Project
from ai_module.models import TestCase

class FunctionalTest(models.Model):
    json_data = models.JSONField(verbose_name="JSON Data")
    origin = models.CharField(max_length=255, verbose_name="Origin")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name='functional_tests', verbose_name="Project")
    test_case = models.ForeignKey(TestCase, on_delete=models.SET_NULL, null=True, related_name='functional_tests', verbose_name="Test Case")
    
    def __str__(self):
        return f"Functional Test for {self.test_case}"

    class Meta:
        verbose_name = "Functional Test"
        verbose_name_plural = "Functional Tests"
        # ordering eliminado para evitar el error de campo inexistente

class Result(models.Model):
    status = models.CharField(max_length=50, verbose_name="Result Status", null=True, blank=True)
    description = models.TextField(verbose_name="Result Description")
    evidence = models.TextField(null=True, blank=True, verbose_name="Evidence")
    test_results = models.JSONField(verbose_name="Test Results")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    functional_test = models.ForeignKey(FunctionalTest, on_delete=models.CASCADE, related_name='results', verbose_name="Functional Test")

    def __str__(self):
        return f"Result for {self.functional_test}"

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"
        ordering = ['created_at']
