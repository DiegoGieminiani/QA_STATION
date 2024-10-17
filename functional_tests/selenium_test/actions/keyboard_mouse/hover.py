from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from functional_test.selenium_test.base_action import BaseAction

class HoverAction(BaseAction):
    def execute(self, element_type, selector_value, timeout=10, **kwargs):
        try:
            # Validar que los parámetros no sean nulos
            if not element_type or not selector_value:
                return self.default_response(
                    action='hover',
                    element=selector_value,
                    status='fail',
                    error="Parámetros inválidos: 'element_type' o 'selector_value' no pueden ser nulos."
                )

            # Obtener el elemento utilizando el método base de la clase
            element = self.get_element(element_type, selector_value)

            # Crear la acción de hover (mover el cursor al elemento)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()

            # Retornar la respuesta estándar de éxito
            return self.default_response(
                action='hover',
                element=selector_value,
                status='success'
            )

        except NoSuchElementException:
            return self.default_response(
                action='hover',
                element=selector_value,
                status='fail',
                error=f"No se encontró el elemento con el selector: {selector_value}"
            )

        except ElementNotInteractableException:
            return self.default_response(
                action='hover',
                element=selector_value,
                status='fail',
                error="El elemento no es interactuable para realizar la acción de hover."
            )

        except TimeoutException:
            return self.default_response(
                action='hover',
                element=selector_value,
                status='fail',
                error="Tiempo de espera agotado. El elemento no fue encontrado para realizar hover."
            )

        except Exception as e:
            return self.default_response(
                action='hover',
                element=selector_value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
