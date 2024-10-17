from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from functional_test.selenium_test.base_action import BaseAction

class EnterDataAction(BaseAction):
    def execute(self, element_type, selector_value, **kwargs):
        # Recibir el valor para ingresar, debe ser flexible
        data = kwargs.get('input_value', '')

        # Validar si se proporcionó un valor de entrada
        if not data:
            return self.default_response(action='enter_data', element=selector_value, status="fail", error="No se proporcionó un valor de entrada.")

        try:
            # Timeout base, configurable según el contexto
            timeout = kwargs.get('timeout', 5)

            # Localizar el elemento
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.get_by_type(element_type, selector_value))
            )

            # Desplazarse al elemento solo si es necesario
            if not element.is_displayed():
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

            # Limpiar el campo antes de ingresar los datos
            element.clear()
            element.send_keys(data)

            # Retornar respuesta de éxito
            return self.default_response(action='enter_data', element=selector_value, status="success", input_value=data)

        except TimeoutException:
            # Manejar el caso en que el elemento no se encuentra en el tiempo esperado
            return self.default_response(action='enter_data', element=selector_value, status="fail", error="Timeout esperando el elemento.")

        except NoSuchElementException:
            # Manejar el caso en que el elemento no se encuentra en la página
            return self.default_response(action='enter_data', element=selector_value, status="fail", error="Elemento no encontrado.")

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(action='enter_data', element=selector_value, status="fail", error=str(e))
