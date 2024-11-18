from django.contrib import admin
from .models import TestCase

# Registra los modelos TestCase y Document en el admin
admin.site.register(TestCase)

