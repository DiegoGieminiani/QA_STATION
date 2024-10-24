from django.shortcuts import render
from django.http import JsonResponse
from functional_tests.runner import TestRunner
from functional_tests.api.serializers import TestRunSerializer
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .process_manual_test_cases import process_manual_test_cases  # Importamos la función que ejecuta las pruebas

# Renderizar la página principal
def main_page(request):
    print("Vista main_page llamada")
    return render(request, 'functional_tests/main.html')

# Ruta que ejecuta las pruebas manualmente desde un formulario
@csrf_exempt
def run_manual_test(request):
    """
    Ruta que genera el formato JSON de pruebas manuales y las ejecuta.
    Acumula las pruebas ejecutadas y genera un reporte con todas las pruebas.
    """
    global manual_test_results  # Usamos una lista global para almacenar los resultados

    if request.method == 'POST':
        try:
            # Obtener los datos del cuerpo de la solicitud como JSON
            body_unicode = request.body.decode('utf-8')
            parameters = json.loads(body_unicode)

            # Validación inicial para verificar estructura mínima del JSON
            if not parameters or not isinstance(parameters, list):
                return JsonResponse({'error': 'El formato de datos proporcionado no es válido.'}, status=400)

            # Validación adicional para comprobar que cada prueba tiene 'url' y 'actions'
            for test in parameters:
                if 'url' not in test or 'actions' not in test:
                    return JsonResponse({'error': 'Cada prueba debe contener "url" y "actions".'}, status=400)

            # Inicializar manual_test_results si no existe previamente
            if 'manual_test_results' not in globals():
                manual_test_results = []

            # Validar el JSON usando el serializer para múltiples pruebas
            try:
                serializer = TestRunSerializer(data=parameters, many=True)
                if serializer.is_valid():
                    # Procesar las pruebas manuales
                    formatted_tests = process_manual_test_cases(serializer.validated_data)

                    # Acumular los resultados de cada prueba manual en la lista global
                    manual_test_results.extend(formatted_tests['individual_results'])

                    # Acumular los resultados globales
                    global_results = [{'id': test.get('id', 'Desconocido'), 'result': test.get('result', 'Desconocido')} for test in manual_test_results]

                    # Devolver el reporte acumulado con resultados individuales y globales
                    return JsonResponse({
                        'individual_results': manual_test_results,
                        'global_results': global_results  # Global con todas las pruebas ejecutadas
                    }, status=200)
                else:
                    # Devolver errores de validación en caso de que el JSON no sea válido
                    return JsonResponse({'errors': serializer.errors}, status=400)
            except Exception as e:
                logging.error(f"Error en la validación del serializer: {str(e)}")
                return JsonResponse({'error': 'Error durante la validación de las pruebas.'}, status=500)

        except json.JSONDecodeError:
            logging.error("Error al decodificar el JSON del cuerpo de la solicitud.")
            return JsonResponse({'error': 'JSON mal formado en la solicitud.'}, status=400)

        except Exception as e:
            logging.error(f"Error procesando las pruebas manuales: {str(e)} - Datos recibidos: {parameters}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

    # Si el método no es POST, devolvemos un error
    return JsonResponse({'error': 'Método inválido. Debes usar POST.'}, status=405)

# Mostrar los resultados de las pruebas
def results_page(request):
    # Asegúrate de que `results` contiene datos válidos
    results = [
        {
            "action": "click",
            "element": "//h5[text()='Forms']",
            "status": "success"
        },
        {
            "action": "click",
            "element": "//span[text()='Practice Form']",
            "status": "success"
        },
        {
            "action": "enter_data",
            "element": "firstName",
            "status": "success",
            "input_value": "John"
        }
        # Más resultados...
    ]
    
    # Pasar los resultados al template
    return render(request, 'functional_tests/results.html', {'results': results})
