def process_manual_test_data(valid_data):
    """
    Procesa el JSON de entrada y prepara los datos para su ejecución.
    Asigna identificadores únicos y filtra los campos con valores `None`.
    """
    processed_tests = []
    test_id_counter = 1
    print("Inicio de process_manual_test_data")  # Indicador de inicio de la función

    # Procesar cada prueba del JSON
    for test in valid_data:
        test_id = f"Prueba {test_id_counter}"
        actions = test.get('actions', [])
        url = test.get('url')

        print(f"Procesando {test_id}:")  # Indica el identificador de la prueba actual
        print("URL:", url)  # Muestra la URL de la prueba actual
        print("Actions antes de limpiar:", actions)  # Muestra las acciones originales

        action_data = []
        for action in actions:
            # Filtrar los campos de cada acción, eliminando valores None
            clean_action = {key: value for key, value in action.items() if value is not None}
            action_data.append(clean_action)
        
        print("Actions después de limpiar:", action_data)  # Muestra las acciones después de limpiar

        # Guardar cada prueba con su ID y las acciones preparadas
        processed_tests.append({
            'id': test_id,
            'url': url,
            'actions': action_data
        })

        test_id_counter += 1

    print("Pruebas procesadas:", processed_tests)  # Muestra todas las pruebas procesadas antes de devolverlas
    return processed_tests
