from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from functional_test.selenium_test.base_action import BaseAction

class ScrollToElementAction(BaseAction):
    def execute(self, element_type, selector_value, timeout=10, **kwargs):
        try:
            # Validar que los parámetros no sean nulos
            if not element_type or not selector_value:
                return self.default_response(
                    action='scroll_to_element',
                    element=selector_value,
                    status='fail',
                    error="Parámetros inválidos: 'element_type' o 'selector_value' no pueden ser nulos."
                )

            # Esperar hasta que el elemento esté presente y visible
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.get_by_type(element_type, selector_value))
            )

            # Ejecutar el script de desplazamiento hasta el elemento
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            
            return self.default_response(
                action='scroll_to_element',
                element=selector_value,
                status='success'
            )
            
        except TimeoutException:
            return self.default_response(
                action='scroll_to_element',
                element=selector_value,
                status="fail",
                error="Timeout: El elemento no se hizo visible a tiempo."
            )
            
        except NoSuchElementException:
            return self.default_response(
                action='scroll_to_element',
                element=selector_value,
                status="fail",
                error="Elemento no encontrado."
            )
            
        except Exception as e:
            return self.default_response(
                action='scroll_to_element',
                element=selector_value,
                status="fail",
                error=f"Error inesperado: {str(e)}"
            )
