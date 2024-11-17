from .runner import TestRunner

def process_automatic_test_cases(valid_data):
    processed_tests = []
    test_id_counter = 1

    for test in valid_data:
        test_id = f"Prueba {test_id_counter}"
        actions = test.get('actions', [])
        url = test.get('url')

        print(f"Procesando {test_id}: URL: {url}, Actions: {actions}")

        processed_tests.append({
            'id': test_id,
            'url': url,
            'actions': actions
        })

        test_id_counter += 1

    results = []
    global_results = []  # Array para manejar los resultados globales de cada prueba

    for test in processed_tests:
        print(f"Ejecutando Prueba {test['id']} con URL: {test['url']}")
        runner = TestRunner({'url': test['url'], 'actions': test['actions']})
        result = runner.run_tests()

        # Guardar los resultados individuales de las acciones
        action_responses = []
        for action_result in result['actions']:
            action_responses.append(action_result)

        # Guardar el resultado individual
        results.append({
            'id': test['id'],
            'url': test['url'],
            'actions': action_responses,  # Respuestas individuales de cada acción
            'result': result['result']
        })

        # Guardar el resultado global de esta prueba
        global_results.append({
            'id': test['id'],
            'result': result['result']
        })

    # Devolver los resultados individuales y el array de resultados globales
    return {
        'individual_results': results,
        'global_results': global_results
    }

