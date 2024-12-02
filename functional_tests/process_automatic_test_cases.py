from .runner import TestRunner
from .models import FunctionalTest, Result
from ai_module.models import TestCase
from user_projects.models import Project

def process_automatic_test_cases(valid_data):
    """
    Procesa casos de prueba automáticos, guarda los datos en la base de datos
    y ejecuta las pruebas para almacenar los resultados.
    """
    processed_tests = []
    test_id_counter = 1

    for test in valid_data:
        test_id = f"Prueba {test_id_counter}"
        actions = test.get('actions', [])
        url = test.get('url')

        print(f"Procesando {test_id}: URL: {url}, Actions: {actions}")

        # Obtener el project_id y test_case_id desde los datos (suponiendo que están incluidos)
        project_id = test.get('project_id')  # Si está en el JSON
        test_case_id = test.get('test_case_id')  # Si está en el JSON

        # Validar que project_id y test_case_id existan en la base de datos
        project = Project.objects.filter(id=project_id).first() if project_id else None
        test_case = TestCase.objects.filter(id=test_case_id).first() if test_case_id else None

        # Guardar en FunctionalTest
        functional_test = FunctionalTest.objects.create(
            json_data=test,
            origin="Automatic",
            project=project,  # Asociar el Project
            test_case=test_case  # Asociar el TestCase
        )

        processed_tests.append({
            'id': test_id,
            'url': url,
            'actions': actions,
            'functional_test_id': functional_test.id
        })

        test_id_counter += 1

    results = []
    global_results = []

    for test in processed_tests:
        print(f"Ejecutando Prueba {test['id']} con URL: {test['url']}")

        # Ejecutar las pruebas con TestRunner
        runner = TestRunner({'url': test['url'], 'actions': test['actions']})
        result = runner.run_tests()

        # Guardar resultados en la base de datos (Result)
        functional_test = FunctionalTest.objects.get(id=test['functional_test_id'])
        test_result = Result.objects.create(
            status=result['result'],
            description=f"Resultado de la prueba {test['id']}",
            test_results=result['actions'],
            functional_test=functional_test
        )

        # Asociar el resultado al FunctionalTest
        functional_test.result = test_result
        functional_test.save()

        # Agregar a los resultados
        results.append({
            'id': test['id'],
            'url': test['url'],
            'actions': result['actions'],
            'result': result['result']
        })

        global_results.append({
            'id': test['id'],
            'result': result['result']
        })

    # Devolver los resultados individuales y globales
    return {
        'individual_results': results,
        'global_results': global_results
    }
