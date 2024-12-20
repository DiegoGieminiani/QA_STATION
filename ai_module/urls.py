from django.urls import path
from . import views  # Importamos las vistas desde views.py

app_name = 'ai_module'

urlpatterns = [
    path('testcases/', views.test_cases_view, name='testcases'), # Ruta para TestCases 
    path('ejecutar-html-processor/', views.ejecutar_html_processor, name='ejecutar_html_processor'),
    path('enviar-json/', views.enviar_json_view, name='enviar_json'), # Ruta para html_processor
    path('add_test_case/<int:project_id>/', views.add_test_case, name='add_test_case')
]

