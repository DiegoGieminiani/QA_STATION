# ai_module/forms.py
from django import forms
from .models import TestCase

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['name', 'actions_data']

        