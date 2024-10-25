
from django.urls import path
from . import views  # Importamos las vistas desde views.py

urlpatterns = [
    path('testcases/', views.test_cases_view, name='testcases'), # Ruta para TestCases 
    path('ejecutar-html-processor/', views.ejecutar_html_processor, name='ejecutar_html_processor'),
    path('enviar-json/', views.enviar_json_view, name='enviar_json'), # Ruta para html_processor
]