from django.utils import timezone
from functional_tests.models import FunctionalTest
from ai_module.models import TestCase
from user_projects.models import Project

def automatic_process(valid_data, project=None, test_case=None):
    test_id_counter = 1

    for test in valid_data:
        test_id = f"Prueba {test_id_counter}"
        actions = test.get('actions', [])
        url = test.get('url')

        # Guardar cada caso de prueba en la base de datos
        FunctionalTest.objects.create(
            json_data={'url': url, 'actions': actions},
            origin='Automatic',  # Ejemplo de valor para el origen
            execution='Pending',  # Estado inicial de ejecución
            project=project,
            test_case=test_case
        )

        test_id_counter += 1

    # Devolver el Test_Case_ID para referencia
    return {
        'test_case_id': test_case_id,
        'status': 'saved',
        'number_of_cases': test_id_counter - 1
    }
