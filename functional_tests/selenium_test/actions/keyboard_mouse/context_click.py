from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from functional_test.selenium_test.base_action import BaseAction

class ContextClickAction(BaseAction):
    def execute(self, element_type, selector_value, timeout=10, **kwargs):
        try:
            # Validar que los parámetros no sean nulos
            if not element_type or not selector_value:
                return self.default_response(
                    action='context_click',
                    element=selector_value,
                    status='fail',
                    error="Parámetros inválidos: 'element_type' o 'selector_value' no pueden ser nulos."
                )

            # Esperar a que el elemento esté presente e interactuable
            element = self.get_element(element_type, selector_value)

            # Crear la acción de context-click (click derecho)
            actions = ActionChains(self.driver)
            actions.context_click(element).perform()

            # Retornar la respuesta estándar de éxito
            return self.default_response(
                action='context_click',
                element=selector_value,
                status='success'
            )

        except NoSuchElementException:
            # Manejar si el elemento no es encontrado
            return self.default_response(
                action='context_click',
                element=selector_value,
                status='fail',
                error=f"No se encontró el elemento con el selector: {selector_value}"
            )

        except ElementNotInteractableException:
            # Manejar si el elemento no es interactuable
            return self.default_response(
                action='context_click',
                element=selector_value,
                status='fail',
                error="El elemento no es interactuable para realizar el context-click."
            )

        except TimeoutException:
            # Manejar si el elemento no está disponible dentro del timeout
            return self.default_response(
                action='context_click',
                element=selector_value,
                status='fail',
                error=f"Timeout al esperar el elemento con selector: {selector_value}"
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='context_click',
                element=selector_value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
