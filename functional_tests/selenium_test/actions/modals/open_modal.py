from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from functional_test.selenium_test.base_action import BaseAction

class OpenModalAction(BaseAction):
    def execute(self, element_type, selector_value, timeout=10, **kwargs):
        try:
            # Validar que los parámetros no sean nulos
            if not element_type or not selector_value:
                return self.default_response(
                    action='open_modal',
                    element=selector_value,
                    status='fail',
                    error="Parámetros inválidos: 'element_type' o 'selector_value' no pueden ser nulos."
                )

            # Esperar a que el elemento que abre el modal sea clicable
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.get_by_type(element_type, selector_value))
            )

            # Hacer clic para abrir el modal
            element.click()

            # Retornar la respuesta estándar de éxito
            return self.default_response(
                action='open_modal',
                element=selector_value,
                status='success'
            )

        except TimeoutException:
            return self.default_response(
                action='open_modal',
                element=selector_value,
                status='fail',
                error="Timeout esperando que el elemento para abrir el modal sea clicable."
            )

        except NoSuchElementException:
            return self.default_response(
                action='open_modal',
                element=selector_value,
                status='fail',
                error="No se encontró el elemento para abrir el modal."
            )

        except ElementClickInterceptedException:
            return self.default_response(
                action='open_modal',
                element=selector_value,
                status='fail',
                error="No se pudo hacer clic en el elemento para abrir el modal."
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='open_modal',
                element=selector_value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
