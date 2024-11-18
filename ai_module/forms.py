# ai_module/forms.py
from django import forms
from .models import TestCase

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['nombre', 'url', 'resultado_esperado', 'functional_test_id']  # Ajusta los nombres de los campos
