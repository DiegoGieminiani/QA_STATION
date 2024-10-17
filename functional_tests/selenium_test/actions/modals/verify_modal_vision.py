
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from functional_test.selenium_test.base_action import BaseAction

class VerifyModalVisibleAction(BaseAction):
    def execute(self, element_type, selector_value, timeout=10, **kwargs):
        try:
            # Validar que los parámetros no sean nulos
            if not element_type or not selector_value:
                return self.default_response(
                    action='verify_modal_visible',
                    element=selector_value,
                    status='fail',
                    error="Parámetros inválidos: 'element_type' o 'selector_value' no pueden ser nulos."
                )

            # Obtener el modal y verificar si está visible
            modal = self.get_element(element_type, selector_value, check_visibility=True)
            is_displayed = modal.is_displayed()

            # Retornar la respuesta basada en la visibilidad del modal
            return self.default_response(
                action='verify_modal_visible',
                element=selector_value,
                status='success' if is_displayed else 'fail'
            )
        
        except NoSuchElementException:
            return self.default_response(
                action='verify_modal_visible',
                element=selector_value,
                status='fail',
                error="No se encontró el modal."
            )

        except TimeoutException:
            return self.default_response(
                action='verify_modal_visible',
                element=selector_value,
                status='fail',
                error="Timeout esperando que el modal sea visible."
            )

        except Exception as e:
            return self.default_response(
                action='verify_modal_visible',
                element=selector_value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
