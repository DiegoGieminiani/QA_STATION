from functional_tests.selenium_test.base_action import BaseAction
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

class SendKeysAction(BaseAction):
    def execute(self, element_type, selector_value, input_value=None, **kwargs):
        try:
            # Validar que el valor de entrada no sea nulo
            if input_value is None:
                return self.default_response(
                    action="send_keys",
                    element=selector_value,
                    status="fail",
                    error="No se proporcionó un 'input_value' para enviar."
                )

            # Usamos get_element de BaseAction para encontrar el elemento
            element = self.get_element(element_type, selector_value)

            # Intentamos enviar las teclas al elemento
            element.send_keys(input_value)

            # Retornamos el resultado de éxito
            return self.default_response(
                action="send_keys",
                element=selector_value,
                status="success",
                input_value=input_value
            )

        except NoSuchElementException:
            # Manejar si el elemento no se encuentra
            return self.default_response(
                action="send_keys",
                element=selector_value,
                status="fail",
                error="Elemento no encontrado."
            )

        except ElementNotInteractableException:
            # Manejar si el elemento no es interactuable
            return self.default_response(
                action="send_keys",
                element=selector_value,
                status="fail",
                error="El elemento no es interactuable."
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action="send_keys",
                element=selector_value,
                status="fail",
                error=f"Error inesperado: {str(e)}"
            )
