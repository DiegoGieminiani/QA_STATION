from functional_test.selenium_test.base_action import BaseAction
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckCheckboxAction(BaseAction):
    def execute(self, driver, locator, value, check=True, **kwargs):
        try:
            # Validar si el locator y el value no son vacíos
            if not locator or not value:
                return self.default_response(action="check_checkbox", element=value, status="fail", error="El localizador o el valor del elemento no son válidos.")

            # Timeout base, configurable según el contexto
            timeout = kwargs.get('timeout', 5)

            # Esperar a que el checkbox esté presente y sea interactuable
            checkbox = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((locator, value))
            )

            # Marcar o desmarcar el checkbox según el parámetro "check"
            if checkbox.is_selected() != check:
                checkbox.click()
                return self.default_response(action="check_checkbox", element=value, status="success", message=f"Checkbox {'marcado' if check else 'desmarcado'} con éxito.")
            else:
                return self.default_response(action="check_checkbox", element=value, status="success", message=f"El checkbox ya estaba {'marcado' if check else 'desmarcado'}.")

        except TimeoutException:
            # Manejar el caso en que el checkbox no está presente en el tiempo esperado
            return self.default_response(action="check_checkbox", element=value, status="fail", error="Timeout esperando al checkbox.")
        
        except NoSuchElementException:
            # Manejar el caso en que el checkbox no se encuentra
            return self.default_response(action="check_checkbox", element=value, status="fail", error="Checkbox no encontrado.")
        
        except ElementNotInteractableException:
            # Manejar el caso en que el checkbox no es interactuable
            return self.default_response(action="check_checkbox", element=value, status="fail", error="El checkbox no es interactuable.")
        
        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(action="check_checkbox", element=value, status="fail", error=f"Error inesperado: {str(e)}")
