from functional_tests.runner import TestRunner

def execute_manual_tests(processed_tests):
    """
    Ejecuta las pruebas manuales utilizando TestRunner y recoge los resultados.
    """
    results = []

    # Ejecutar cada prueba procesada
    for test in processed_tests:
        print(f"Ejecutando {test['id']}: URL: {test['url']}, Actions: {test['actions']}")

        # Crear instancia de TestRunner y ejecutar la prueba
        runner = TestRunner({'url': test['url'], 'actions': test['actions']})
        result = runner.run_tests()

        # Procesar los resultados de la ejecución
        action_responses = []
        for action_result in result['actions']:
            action_data = {
                'action': action_result.get('action'),
                'element': action_result.get('element'),
                'status': action_result.get('status', 'unknown')
            }
            if action_result.get('input_value') is not None:
                action_data['input_value'] = action_result.get('input_value')
            if action_result.get('actual_value') is not None:
                action_data['actual_value'] = action_result.get('actual_value')
            
            action_responses.append(action_data)

        # Agregar el resultado de cada prueba al conjunto de resultados
        results.append({
            'id': test['id'],
            'url': test['url'],
            'actions': action_responses,
            'result': result['result']
        })

    # Devolver los resultados individuales y globales
    return {
        'individual_results': results,
        'global_results': [{'id': test['id'], 'result': test['result']} for test in results]
    }
