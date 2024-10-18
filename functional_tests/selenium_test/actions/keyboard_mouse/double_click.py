from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from functional_tests.selenium_test.base_action import BaseAction

class DoubleClickAction(BaseAction):
    def execute(self, element_type, selector_value, timeout=10, **kwargs):
        try:
            # Validar que los parámetros no sean nulos
            if not element_type or not selector_value:
                return self.default_response(
                    action='double_click',
                    element=selector_value,
                    status='fail',
                    error="Parámetros inválidos: 'element_type' o 'selector_value' no pueden ser nulos."
                )

            # Obtener el tipo de localizador y el selector
            by_type, selector = self.get_by_type(element_type, selector_value)
            
            # Esperar hasta que el elemento sea visible y clicable
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by_type, selector))
            )
            
            # Crear la acción de doble-click
            actions = ActionChains(self.driver)
            actions.double_click(element).perform()
            
            # Retornar la respuesta estándar de éxito
            return self.default_response(
                action='double_click',
                element=selector_value,
                status='success'
            )

        except TimeoutException:
            # Manejar el timeout si el elemento no es clicable en el tiempo dado
            return self.default_response(
                action='double_click',
                element=selector_value,
                status='fail',
                error="Tiempo de espera agotado. El elemento no fue clicable."
            )

        except NoSuchElementException:
            # Manejar si el elemento no es encontrado
            return self.default_response(
                action='double_click',
                element=selector_value,
                status='fail',
                error=f"No se encontró el elemento con el selector: {selector_value}"
            )

        except ElementNotInteractableException:
            # Manejar si el elemento no es interactuable
            return self.default_response(
                action='double_click',
                element=selector_value,
                status='fail',
                error="El elemento no es interactuable para realizar el doble-click."
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='double_click',
                element=selector_value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
