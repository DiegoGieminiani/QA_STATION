from django.contrib import admin
from .models import TestCase, Document

# Registra los modelos TestCase y Document en el admin
admin.site.register(TestCase)
admin.site.register(Document)
