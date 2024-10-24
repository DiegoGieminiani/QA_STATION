from functional_tests.runner import TestRunner

def process_manual_test_cases(valid_data):
    """
    Procesa las pruebas manuales ejecutando las acciones con el TestRunner.
    Filtra los campos con valores `None` para que el formato coincida con el flujo automático.
    """
    processed_tests = []
    test_id_counter = 1

    # Procesar cada prueba del JSON
    for test in valid_data:
        test_id = f"Prueba {test_id_counter}"
        actions = test.get('actions', [])
        url = test.get('url')

        print(f"Ejecutando Prueba {test_id}: URL: {url}, Actions: {actions}")

        # Ejecutar las acciones usando TestRunner en cada prueba
        runner = TestRunner({'url': url, 'actions': actions})
        result = runner.run_tests()

        # Guardar los resultados de las acciones ejecutadas, filtrando campos con valores None
        action_responses = []
        for action_result in result['actions']:
            action_data = {
                'action': action_result.get('action'),
                'element': action_result.get('element'),
                'status': action_result.get('status', 'unknown')
            }

            # Solo agregar 'input_value' si tiene un valor
            if action_result.get('input_value') is not None:
                action_data['input_value'] = action_result.get('input_value')

            # Solo agregar 'actual_value' si tiene un valor
            if action_result.get('actual_value') is not None:
                action_data['actual_value'] = action_result.get('actual_value')

            action_responses.append(action_data)

        # Determinar el resultado de la prueba
        test_result = result['result']

        # Guardar los resultados de cada prueba ejecutada
        processed_tests.append({
            'id': test_id,
            'url': url,
            'actions': action_responses,  # Lista completa de las acciones ejecutadas
            'result': test_result
        })

        test_id_counter += 1

    # Devolver los resultados individuales y globales
    return {
        'individual_results': processed_tests,
        'global_results': [{'id': test['id'], 'result': test['result']} for test in processed_tests]
    }
