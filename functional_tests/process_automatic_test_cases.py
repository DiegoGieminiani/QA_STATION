from .runner import TestRunner
from .models import FunctionalTest, Result
from ai_module.models import TestCase
from user_projects.models import Project

def process_automatic_test_cases(valid_data):
    """
    Procesa casos de prueba automáticos, relaciona datos del JSON con las tablas
    `ai_module_testcase` y `user_projects_project`, y guarda los datos correctamente.
    """
    processed_tests = []
    test_id_counter = 1

    for test in valid_data:
        test_id = f"Prueba {test_id_counter}"
        actions = test.get('actions', [])
        url = test.get('url')

        print(f"Procesando {test_id}: URL: {url}, Actions: {actions}")

        # Buscar el TestCase relacionado en ai_module_testcase usando la URL
        test_case = TestCase.objects.filter(name=url).order_by('-id').first()  # Usamos order_by para tomar el último registro en caso de duplicados

        if not test_case:
            print(f"Error: No se encontró un TestCase para la URL: {url}")
            continue

        # Obtener el project_id desde el TestCase
        project_id = test_case.project_id  # Relación directa
        project = Project.objects.filter(id=project_id).first()

        if not project:
            print(f"Error: No se encontró un Project con ID: {project_id} para la prueba {test_id}")
            continue

        # Guardar en FunctionalTest
        functional_test = FunctionalTest.objects.create(
            json_data=test,
            origin="Automatic",
            project=project,
            test_case=test_case
        )

        processed_tests.append({
            'id': test_id,
            'url': url,
            'actions': actions,
            'functional_test_id': functional_test.id
        })

        test_id_counter += 1

    # Manejo de resultados de pruebas
    results = []
    global_results = []

    for test in processed_tests:
        print(f"Ejecutando Prueba {test['id']} con URL: {test['url']}")

        # Ejecutar las pruebas con TestRunner
        runner = TestRunner({'url': test['url'], 'actions': test['actions']})
        result = runner.run_tests()

        # Guardar resultados en la base de datos
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
