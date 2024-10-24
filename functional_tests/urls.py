from django.urls import path, include
from .views import main_page, results_page, run_manual_test  # Importa correctamente las vistas

urlpatterns = [
    path('', main_page, name='main_page'),  # Ruta para la interfaz principal
    path('results/', results_page, name='results_page'),  # Ruta para la página de resultados
    path('run/', run_manual_test, name='run_manual_test'),  # Ruta para ejecutar las pruebas manualmente
    path('api/', include('functional_tests.api.api_urls')),  # Ruta para la API (para los datos que llegan de otro módulo)
]
