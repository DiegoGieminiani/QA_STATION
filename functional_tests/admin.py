from django.contrib import admin
from .models import FunctionalTest, Result

# Registra los modelos FunctionalTest y Result en el admin
admin.site.register(FunctionalTest)
admin.site.register(Result)