from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from functional_tests.models import FunctionalTest, Result
from functional_tests.api.serializers import TestRunSerializer
import json
import logging


def main_page(request):
    """
    Renderiza la página principal de functional_tests.
    """
    print("Vista main_page llamada")
    return render(request, 'functional_tests/main.html')


@csrf_exempt
def run_manual_test(request):
    """
    Maneja la ejecución de pruebas manuales.
    Guarda los datos en la base de datos y devuelve un reporte acumulado.
    """
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud
            body_unicode = request.body.decode('utf-8')
            parameters = json.loads(body_unicode)

            # Validar que el JSON contenga pruebas válidas
            serializer = TestRunSerializer(data=parameters, many=True)
            if serializer.is_valid():
                validated_data = serializer.validated_data

                # Procesar y guardar pruebas en la base de datos
                individual_results = []
                global_results = []

                for test in validated_data:
                    # Crear registro de FunctionalTest
                    functional_test = FunctionalTest.objects.create(
                        json_data=test,
                        origin="Manual",
                        execution="In Progress"
                    )

                    # Simular ejecución de prueba y obtener resultados
                    actions = test.get("actions", [])
                    url = test.get("url")
                    results = []  # Aquí llamarías a `TestRunner` o lógica manual

                    for action in actions:
                        result = {
                            "action": action.get("action"),
                            "status": "success",  # Simulación del resultado
                            "element": action.get("value"),
                            "input_value": action.get("input_value", None),
                            "error": None
                        }
                        results.append(result)

                    # Crear resultado global
                    global_status = "success" if all(res["status"] == "success" for res in results) else "fail"
                    result_record = Result.objects.create(
                        status=global_status,
                        description=f"Resultados de la prueba manual para {url}",
                        test_results=results,
                        functional_test=functional_test
                    )

                    # Actualizar estado de ejecución
                    functional_test.execution = "Completed"
                    functional_test.result = result_record
                    functional_test.save()

                    # Agregar a las listas de resultados acumulados
                    individual_results.extend(results)
                    global_results.append({"id": functional_test.id, "result": global_status})

                # Devolver reporte
                return JsonResponse({
                    "individual_results": individual_results,
                    "global_results": global_results
                }, status=200)
            else:
                # Errores de validación
                return JsonResponse({"errors": serializer.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON mal formado en la solicitud."}, status=400)

        except Exception as e:
            logging.error(f"Error procesando pruebas manuales: {str(e)}")
            return JsonResponse({"error": f"Error interno: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método inválido. Debes usar POST."}, status=405)




from django.core.serializers.json import DjangoJSONEncoder
import json

def results_page(request):
    try:
        # Obtener resultados desde la base de datos
        results = Result.objects.select_related("functional_test").all()

        # Preparar datos para la plantilla
        results_data = []
        for result in results:
            test_results = result.test_results
            print(f"Test Results for FunctionalTest {result.functional_test.id}: {test_results}")
            for action_result in test_results:
                results_data.append({
                    "functional_test": result.functional_test.id,
                    "action": action_result.get("action"),
                    "element": action_result.get("element"),
                    "status": action_result.get("status"),
                    "input_value": action_result.get("input_value", None),
                    "error": action_result.get("error", None)
                })

        print(f"Results Data Prepared: {results_data}")
        return render(request, "functional_tests/results.html", {"results": results_data})
    except Exception as e:
        logging.error(f"Error al cargar los resultados: {str(e)}")
        return render(request, "functional_tests/results.html", {"results": []})
