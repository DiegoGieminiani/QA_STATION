from django.shortcuts import render
from django.http import JsonResponse
from functional_test.runner import TestRunner  # Orquestador de las pruebas
from functional_test.api.serializers import TestRunSerializer  # Serializer para los datos de las pruebas
import logging
import json

# Renderizar la página principal
def main_page(request):
    print("Vista main_page llamada")
    return render(request, 'functional_tests/main.html')

# Ruta que ejecuta las pruebas manualmente desde un formulario
def run_tests(request):
    """
    Ruta que ejecuta las pruebas manualmente cuando se envían desde el formulario.
    """
    if request.method == 'POST':
        try:
            # Obtener los datos del cuerpo de la solicitud como JSON
            body_unicode = request.body.decode('utf-8')
            parameters = json.loads(body_unicode)  # Convertir los datos JSON a un diccionario Python

            # Depurar los datos recibidos para verificar que llegan correctamente
            print("Datos recibidos en el formulario:", parameters)

            # Verificar que los datos básicos estén presentes
            if not parameters.get('url') or not parameters.get('actions'):
                print("Faltan parámetros obligatorios (URL o acciones)")
                return JsonResponse({'error': 'Faltan parámetros obligatorios (URL o acciones)'}, status=400)

            # Procesar las acciones y preparar los datos para el serializer
            actions = parameters['actions']

            data = {
                'url': parameters.get('url'),
                'actions': actions
            }

            # Depurar los datos que se están enviando al serializer
            print("Datos preparados para el serializer:", data)

            # Validar los datos usando el serializer
            serializer = TestRunSerializer(data=data)
            if serializer.is_valid():
                print("Datos validados correctamente por el serializer")

                # Ejecutar las pruebas si los datos son válidos
                runner = TestRunner(serializer.validated_data)
                results = runner.run_tests()  # Ejecutar las pruebas
                print("Resultados de las pruebas:", results)
                return JsonResponse({'results': results})
            else:
                print("Errores de validación del serializer:", serializer.errors)
                # Retornar los errores de validación si los datos no son válidos
                return JsonResponse({'errors': serializer.errors}, status=400)

        except Exception as e:
            # Registrar cualquier error ocurrido durante la ejecución
            logging.error(f"Error ejecutando las pruebas: {str(e)}")
            print(f"Excepción capturada: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    # Si no es una solicitud POST, devolver un error
    print("Método no válido. Se esperaba POST.")
    return JsonResponse({'error': 'Método inválido'}, status=405)

# Mostrar los resultados de las pruebas
def results_page(request):
    return render(request, 'functional_tests/results.html')
