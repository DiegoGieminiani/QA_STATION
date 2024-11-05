from django.utils import timezone

def automatic_process(valid_data, project=None, test_case=None):
    # Importa FunctionalTest dentro de la función
    from functional_tests.models import FunctionalTest

    test_id_counter = 1
    print("Inicio de automatic_process")  # Indicador de inicio de la función

    for test in valid_data:
        test_id = f"Prueba {test_id_counter}"
        actions = test.get('actions', [])
        url = test.get('url')

        print(f"Procesando {test_id}:")  # Indica qué prueba se está procesando
        print("URL:", url)  # Muestra la URL de la prueba actual
        print("Actions:", actions)  # Muestra las acciones de la prueba actual

        # Guardar cada caso de prueba en la base de datos
        try:
            FunctionalTest.objects.create(
                json_data={'url': url, 'actions': actions},
                origin='Automatic',  # Ejemplo de valor para el origen
                project=project,
                test_case=test_case
            )
            print(f"{test_id} guardado en la base de datos.")  # Confirmación de guardado
        except Exception as e:
            print(f"Error al guardar {test_id}: {str(e)}")  # Muestra cualquier error al guardar

        test_id_counter += 1

    # Devolver el Test_Case_ID para referencia
    resultado = {
        'test_case_id': test_case,
        'status': 'saved',
        'number_of_cases': test_id_counter - 1
    }
    print("Resultado de automatic_process:", resultado)  # Muestra el resultado final antes de devolverlo

