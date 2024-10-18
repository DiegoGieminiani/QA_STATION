from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from functional_tests.selenium_test.base_action import BaseAction

class ClearFieldAction(BaseAction):
    def execute(self, driver, locator, value, **kwargs):
        try:
            # Validar si el locator y el value no son vacíos
            if not locator or not value:
                return self.default_response(action='clear_field', element=value, status="fail", error="El localizador o el valor del elemento no son válidos.")

            # Timeout base, configurable según el contexto
            timeout = kwargs.get('timeout', 5)

            # Esperar hasta que el elemento esté presente
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((locator, value))
            )

            # Limpiar el campo
            element.clear()

            # Retornar respuesta de éxito
            return self.default_response(action='clear_field', element=value, status="success")

        except TimeoutException:
            # Manejar el caso en que el elemento no se encuentra en el tiempo esperado
            return self.default_response(action='clear_field', element=value, status="fail", error="Timeout esperando al elemento.")
        
        except NoSuchElementException:
            # Manejar el caso en que el elemento no se encuentra
            return self.default_response(action='clear_field', element=value, status="fail", error="Elemento no encontrado.")

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(action='clear_field', element=value, status="fail", error=str(e))
