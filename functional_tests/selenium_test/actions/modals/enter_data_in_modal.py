from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from functional_test.selenium_test.base_action import BaseAction

class EnterDataInModalAction(BaseAction):
    def execute(self, element_type, selector_value, input_value, **kwargs):
        try:
            # Validar que los parámetros no sean nulos
            if not element_type or not selector_value or not input_value:
                return self.default_response(
                    action='enter_data_in_modal',
                    element=selector_value,
                    status='fail',
                    error="Parámetros inválidos: 'element_type', 'selector_value' y 'input_value' no pueden ser nulos."
                )

            # Obtener el campo de entrada en el modal
            input_field = self.get_element(element_type, selector_value)
            
            # Limpiar y enviar el nuevo valor
            input_field.clear()
            input_field.send_keys(input_value)

            # Retornar la respuesta de éxito
            return self.default_response(
                action='enter_data_in_modal',
                element=selector_value,
                status='success',
                input_value=input_value
            )
        
        except NoSuchElementException:
            return self.default_response(
                action='enter_data_in_modal',
                element=selector_value,
                status='fail',
                error="No se encontró el campo de entrada en el modal."
            )

        except ElementNotInteractableException:
            return self.default_response(
                action='enter_data_in_modal',
                element=selector_value,
                status='fail',
                error="El campo de entrada no es interactuable."
            )
        
        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='enter_data_in_modal',
                element=selector_value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
