from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from functional_tests.selenium_test.base_action import BaseAction


class EnterDataAction(BaseAction):
    def execute(self, element_type, selector_value, **kwargs):
        data = kwargs.get('input_value', '')

        if not data:
            return self.default_response(action='enter_data', element=selector_value, status="fail", error="No se proporcionó un valor de entrada.")

        try:
            timeout = kwargs.get('timeout', 10)

            # Usar `element_to_be_clickable` en lugar de `presence_of_element_located`
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.get_by_type(element_type, selector_value))
            )

            # Desplazarse al elemento solo si es necesario
            if not element.is_displayed():
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

            # Limpiar el campo antes de ingresar los datos
            element.clear()
            element.send_keys(data)

            return self.default_response(action='enter_data', element=selector_value, status="success", input_value=data)

        except TimeoutException:
            return self.default_response(action='enter_data', element=selector_value, status="fail", error=f"Timeout después de {timeout} segundos esperando el elemento.")

        except NoSuchElementException:
            return self.default_response(action='enter_data', element=selector_value, status="fail", error="Elemento no encontrado en la página.")

        except ElementNotInteractableException:
            return self.default_response(action='enter_data', element=selector_value, status="fail", error="El elemento está presente pero no es interactuable.")

        except Exception as e:
            return self.default_response(action='enter_data', element=selector_value, status="fail", error=f"Error inesperado: {str(e)}")
