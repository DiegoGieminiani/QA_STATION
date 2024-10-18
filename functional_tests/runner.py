from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .helper import initialize_chrome_driver  # Helper para inicializar el navegador
from .action_handler import execute_action  # Ejecutar acciones
from .action_handler import resolve_variables  # Resolver variables dinámicas
from .action_handler import retry_action  # Manejador de reintentos
from .action_handler import handle_alert  # Manejador de alertas (si aplica)
from functional_tests.action_router import ActionRouter 

class TestRunner:
    def __init__(self, json_data, retry_attempts=3):
        self.driver = initialize_chrome_driver()  # Inicializamos el navegador
        self.actions = json_data.get('actions', [])  # Las acciones que se ejecutarán
        self.url = json_data['url']  # URL de la página a probar
        self.retry_attempts = retry_attempts  # Cantidad de reintentos
        self.stored_values = {}  # Almacena valores dinámicos durante la ejecución
        self.test_results = []  # Almacena los resultados de las pruebas
        self.router = ActionRouter(self.driver)  # Pasar el driver al enrutador

    def log_message(self, message):
        """Método para registrar mensajes en el log."""
        print(f"LOG: {message}")

    def start_browser(self):
        """Abrir el navegador en la URL de prueba."""
        self.log_message(f"Abriendo la URL: {self.url}")
        self.driver.get(self.url)

    def close_browser(self):
        """Cerrar el navegador después de las pruebas."""
        self.driver.quit()

    def handle_single_action(self, action):
        """Manejar la ejecución de una sola acción."""
        # Enrutar la acción usando ActionRouter
        action_instance = self.router.route_action(action['action']) 
        
        if not action_instance:
            log_message = f"Acción {action['action']} no está definida en el router."
            self.log_message(log_message)
            return {'action': action['action'], 'status': 'fail', 'message': log_message}

        element_type = action.get('element_type')
        selector_value = action.get('value')
        kwargs = {k: v for k, v in action.items() if k not in ['action', 'element_type', 'value']}
        kwargs = resolve_variables(self.stored_values, kwargs)

        # Debug: Verificar los parámetros que se están pasando a la acción
        self.log_message(f"Ejecutando acción: {action['action']} con params: {kwargs}")

        # Manejo de alertas si aplica
        alert_result = handle_alert(self.driver, action['action'], self.log_message)
        if alert_result:
            return alert_result

        # Ejecutar la acción y manejar reintentos
        result = retry_action(
            execute_action, self.retry_attempts, self.log_message, action_instance, action['action'],
            element_type=element_type, selector_value=selector_value, **kwargs
        )
        
        # Si la acción tiene texto extraído, almacenarlo
        if result.get('status') == 'success' and 'extracted_text' in result:
            variable_name = action.get('variable_name')
            if variable_name:
                self.stored_values[variable_name] = result['extracted_text']
        
        return result

    def execute_all_actions(self):
        """Ejecutar todas las acciones definidas."""
        for action in self.actions:
            result = self.handle_single_action(action)
            self.test_results.append(result)

    def run_tests(self):
        """Método principal para correr las pruebas."""
        try:
            self.start_browser()
            self.execute_all_actions()
        finally:
            self.close_browser()
        
        self.log_message("TEST COMPLETADO")
        return self.test_results
