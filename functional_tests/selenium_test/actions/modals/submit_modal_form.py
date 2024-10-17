from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from functional_test.selenium_test.base_action import BaseAction

class SubmitModalFormAction(BaseAction):
    def execute(self, element_type, selector_value, timeout=10, **kwargs):
        try:
            # Validar que los parámetros no sean nulos
            if not element_type or not selector_value:
                return self.default_response(
                    action='submit_modal_form',
                    element=selector_value,
                    status='fail',
                    error="Parámetros inválidos: 'element_type' o 'selector_value' no pueden ser nulos."
                )

            # Obtener el botón de envío dentro del modal
            submit_button = self.get_element(element_type, selector_value)
            
            # Hacer clic en el botón para enviar el formulario
            submit_button.click()

            # Retornar la respuesta estándar de éxito
            return self.default_response(
                action='submit_modal_form',
                element=selector_value,
                status='success'
            )

        except TimeoutException:
            return self.default_response(
                action='submit_modal_form',
                element=selector_value,
                status='fail',
                error="Timeout esperando el botón de envío del formulario modal."
            )

        except NoSuchElementException:
            return self.default_response(
                action='submit_modal_form',
                element=selector_value,
                status='fail',
                error="No se encontró el botón de envío en el modal."
            )

        except ElementClickInterceptedException:
            return self.default_response(
                action='submit_modal_form',
                element=selector_value,
                status='fail',
                error="No se pudo hacer clic en el botón de envío del formulario modal."
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='submit_modal_form',
                element=selector_value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
