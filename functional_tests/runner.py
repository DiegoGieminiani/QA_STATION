from selenium.common.exceptions import TimeoutException, NoSuchElementException
from functional_tests.selenium_test.helper import initialize_chrome_driver
from .action_handler import execute_action, resolve_variables, retry_action, handle_alert
from functional_tests.action_router import ActionRouter
import time

class TestRunner:
    def __init__(self, json_data, retry_attempts=3):
        self.driver = initialize_chrome_driver()  # Inicializamos el navegador
        self.actions = json_data.get('actions', [])  # Las acciones que se ejecutarán
        self.url = json_data.get('url', '')  # URL de la página a probar
        self.retry_attempts = retry_attempts  # Cantidad de reintentos
        self.stored_values = {}  # Almacena valores dinámicos durante la ejecución
        self.test_results = []  # Almacena los resultados de las pruebas
        self.router = ActionRouter(self.driver)  # Pasar el driver al enrutador
        self.test_completed = False  # Asegura que las pruebas se ejecutan solo una vez

    def log_message(self, message):
        """Método para registrar mensajes en el log."""
        print(f"LOG: {message}")

    def start_browser(self):
        """Abrir el navegador en la URL de prueba."""
        self.log_message(f"Abriendo la URL: {self.url}")
        try:
            self.driver.get(self.url)
        except Exception as e:
            self.log_message(f"Error al abrir la URL: {e}")
            raise

    def close_browser(self):
        """Cerrar el navegador después de las pruebas."""
        if self.driver:  # Aseguramos que el driver esté activo antes de cerrarlo
            self.log_message("Cerrando el navegador.")
            try:
                self.driver.quit()
            except Exception as e:
                self.log_message(f"Error al cerrar el navegador: {e}")
            self.driver = None
    def handle_single_action(self, action):
        """Manejar la ejecución de una sola acción."""
        action_name = action.get('action')
        
        # Filtrar los parámetros para pasar solo los necesarios
        params = {key: action[key] for key in action if key not in ['action', 'element_type', 'value']}
        
        # Si la acción es 'navigate_to_url', agregar la URL a params
        if action_name == 'navigate_to_url':
            params['url'] = self.url  # Asegúrate de pasar la URL correcta aquí

        action_instance = self.router.route_action(action_name, params)

        if not action_instance:
            self.log_message(f"Acción {action_name} no está definida en el router.")
            return {'action': action_name, 'status': 'fail', 'message': 'Acción no definida'}

        # Obtener el tipo de elemento y el valor del selector
        element_type = action.get('element_type')
        selector_value = action.get('value')

        # Extraer kwargs para los parámetros adicionales
        kwargs = {k: v for k, v in action.items() if k not in ['action', 'element_type', 'value']}
        kwargs = resolve_variables(self.stored_values, kwargs)

        # Depurar los parámetros para ver si se están pasando correctamente
        self.log_message(f"Ejecutando acción: {action_name} con params: {params}")

        try:
            # Llamada a execute_action, pasando la URL u otros parámetros necesarios
            response = execute_action(action_instance, action_name, element_type, selector_value, **params)
            return response  # Retornar el resultado de la ejecución

        except Exception as e:
            self.log_message(f"Error inesperado en la ejecución de {action_name}: {e}")
            return {'action': action_name, 'status': 'fail', 'message': str(e)}

        
    #Automático
    def execute_all_actions(self):
        """Ejecutar todas las acciones definidas."""
        for action in self.actions:
            result = self.handle_single_action(action)
            if result:  # Asegurarse de que haya un resultado válido
                self.log_message(f"Resultado agregado a test_results: {result}")
                self.test_results.append(result)
            else:
                self.log_message(f"Acción {action.get('action')} no produjo ningún resultado válido.")

        if not self.test_results:
            self.log_message("Error: La lista test_results sigue vacía después de ejecutar las acciones.")
        else:
            self.log_message(f"test_results llenado correctamente con {len(self.test_results)} resultados.")

    def run_tests(self):
        """Método principal para correr las pruebas."""
        if not self.test_completed:  # Evitar múltiples ejecuciones de pruebas
            try:
                self.start_browser()  # Abrir el navegador en la URL de prueba
                self.execute_all_actions()  # Ejecutar todas las acciones
            finally:
                self.close_browser()  # Cerrar el navegador

            if not self.test_results:
                self.log_message("Error: Lista de resultados vacía después de ejecutar todas las acciones.")
                return {'result': 'fail', 'message': 'No se pudieron obtener resultados de las acciones.'}
            else:
                self.log_message(f"test_results contiene {len(self.test_results)} resultados.")

            # Verificar si todas las acciones fueron exitosas
            all_success = all(result['status'] == 'success' for result in self.test_results)
            test_result = 'success' if all_success else 'fail'

            self.test_completed = True

            # Devolver los resultados de la prueba
            result_data = {
                'actions': self.test_results,
                'result': test_result
            }

            self.log_message(f"Devolviendo result_data: {result_data}")
            return result_data

        else:
            self.log_message("Pruebas ya ejecutadas. No se ejecutarán nuevamente.")
            return {
                'actions': self.test_results,
                'result': 'Pruebas ya ejecutadas'
            }
