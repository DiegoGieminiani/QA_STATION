from django.urls import path
from . import views

app_name = 'ai_module'

urlpatterns = [
    path('testcases/<int:project_id>/', views.test_cases_view, name='testcases'),
    path('ejecutar-html-processor/<int:project_id>/', views.ejecutar_html_processor, name='ejecutar_html_processor'),
    path('enviar-json/', views.enviar_json_view, name='enviar_json'),
    path('add_test_case/<int:project_id>/', views.add_test_case, name='add_test_case'),
]

