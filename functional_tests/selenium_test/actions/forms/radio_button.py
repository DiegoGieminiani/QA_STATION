from functional_test.selenium_test.base_action import BaseAction
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SelectRadioButtonAction(BaseAction):
    def execute(self, driver, locator, value, **kwargs):
        try:
            # Validar si el locator y el value no son vacíos
            if not locator or not value:
                return self.default_response(action="select_radio_button", element=value, status="fail", error="El localizador o el valor del elemento no son válidos.")

            # Timeout base, configurable según el contexto
            timeout = kwargs.get('timeout', 5)

            # Esperar a que el radio button esté presente y sea interactuable
            radio_button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((locator, value))
            )

            # Verificar si el radio button no está ya seleccionado
            if not radio_button.is_selected():
                radio_button.click()
                return self.default_response(action="select_radio_button", element=value, status="success", message="Radio button seleccionado con éxito.")
            else:
                return self.default_response(action="select_radio_button", element=value, status="success", message="El radio button ya estaba seleccionado.")

        except TimeoutException:
            # Manejar el caso en que el radio button no está presente en el tiempo esperado
            return self.default_response(action="select_radio_button", element=value, status="fail", error="Timeout esperando al radio button.")
        
        except NoSuchElementException:
            # Manejar el caso en que el radio button no se encuentra
            return self.default_response(action="select_radio_button", element=value, status="fail", error="Radio button no encontrado.")
        
        except ElementNotInteractableException:
            # Manejar el caso en que el radio button no es interactuable
            return self.default_response(action="select_radio_button", element=value, status="fail", error="El radio button no es interactuable.")
        
        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(action="select_radio_button", element=value, status="fail", error=f"Error inesperado: {str(e)}")
