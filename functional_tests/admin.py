from django.contrib import admin
from .models import FunctionalTest, Result, Action

# Registra los modelos FunctionalTest y Action en el admin
@admin.register(FunctionalTest)
class FunctionalTestAdmin(admin.ModelAdmin):
    list_display = ('functional_test_id', 'url', 'project')

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('action_id', 'action', 'functional_test')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('status', 'description', 'action')
