from django.db import models
from user_projects.models import Project

class TestCase(models.Model):
    name = models.CharField(max_length=255, verbose_name="Test Case Name")
    actions_data = models.JSONField(verbose_name="Actions Data")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='test_cases', verbose_name="Project")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Test Case"
        verbose_name_plural = "Test Cases"
        ordering = ['name']

class Document(models.Model):
    name = models.CharField(max_length=255, verbose_name="Document Name")
    document_url = models.URLField(verbose_name="Document URL")
    document_type = models.CharField(max_length=50, verbose_name="Document Type")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    test_case = models.OneToOneField(TestCase, on_delete=models.CASCADE, related_name='document', verbose_name="Test Case")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['name']
