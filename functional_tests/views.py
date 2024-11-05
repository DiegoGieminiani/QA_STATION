from django.shortcuts import render
from functional_tests.runner import TestRunner
import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from functional_tests.manual_test.manual_process import process_manual_test_data
from functional_tests.manual_test.manual_execution_handler import execute_manual_tests
from functional_tests.automatic_test.serializers.test_run_serializers import TestRunSerializer


def main_page(request):
    print("Vista main_page llamada")
    return render(request, 'functional_tests/main.html')

# Lista global para acumular los resultados de las pruebas manuales
#manual_test_results = []
@csrf_exempt
def run_manual_test(request):
    """
    Ruta que genera el formato JSON de pruebas manuales y las ejecuta.
    Genera un reporte con los resultados de las pruebas de la ejecución actual.
    """
    if request.method == 'POST':
        try:
            # Obtener los datos del cuerpo de la solicitud como JSON
            body_unicode = request.body.decode('utf-8')
            parameters = json.loads(body_unicode)
            print("Datos recibidos:", parameters)

            # Validación inicial para verificar la estructura mínima del JSON
            if not parameters or not isinstance(parameters, list):
                print("Error: Formato de datos no válido.")
                return JsonResponse({'error': 'El formato de datos proporcionado no es válido.'}, status=400)

            # Validación adicional para comprobar que cada prueba tiene 'url' y 'actions'
            for test in parameters:
                if 'url' not in test or 'actions' not in test:
                    print("Error: Falta 'url' o 'actions' en una de las pruebas.")
                    return JsonResponse({'error': 'Cada prueba debe contener "url" y "actions".'}, status=400)

            # Validar el JSON usando el serializer para múltiples pruebas
            serializer = TestRunSerializer(data=parameters, many=True)
            if not serializer.is_valid():
                print("Errores de validación:", serializer.errors)
                return JsonResponse({'errors': serializer.errors}, status=400)

            print("Datos validados correctamente:", serializer.validated_data)

            # Procesar el JSON de entrada
            processed_tests = process_manual_test_data(serializer.validated_data)
            print("Pruebas procesadas:", processed_tests)

            # Ejecutar las pruebas y obtener los resultados de la ejecución actual
            results = execute_manual_tests(processed_tests)
            print("Resultados de ejecución:", results)

            # Generar los resultados individuales y globales de la ejecución actual
            individual_results = results['individual_results']
            global_results = [{'id': test.get('id', 'Desconocido'), 'result': test.get('result', 'Desconocido')} for test in individual_results]
            print("Resultados individuales actuales:", individual_results)
            print("Resultados globales actuales:", global_results)

            # Devolver el reporte de la ejecución actual con resultados individuales y globales
            return JsonResponse({
                'individual_results': individual_results,
                'global_results': global_results
            }, status=200)

        except json.JSONDecodeError:
            logging.error("Error al decodificar el JSON del cuerpo de la solicitud.")
            print("Error: JSON mal formado en la solicitud.")
            return JsonResponse({'error': 'JSON mal formado en la solicitud.'}, status=400)

        except Exception as e:
            logging.error(f"Error procesando las pruebas manuales: {str(e)} - Datos recibidos: {parameters}")
            print(f"Error interno: {str(e)}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

    print("Error: Método inválido. Debes usar POST.")
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
