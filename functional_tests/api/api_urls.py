from django.urls import path
from .api_views import ExecuteTestsAPI

urlpatterns = [
    path('run-tests/', ExecuteTestsAPI.as_view(), name='run_tests_api'),  # Ejecutar pruebas
]
