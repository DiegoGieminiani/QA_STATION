from functional_test.selenium_test.base_action import BaseAction
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from functional_test.selenium_test.waits.explicit_wait import ExplicitWaitAction

class SelectAction(BaseAction):
    def execute(self, element_type, selector_value, input_value=None, timeout=10, **kwargs):
        try:
            # Validar que los parámetros sean válidos
            if not element_type or not selector_value:
                return self.default_response(
                    action='select',
                    element=selector_value,
                    status='fail',
                    error="El tipo de elemento o el valor del selector no son válidos."
                )
            
            # Usar la acción de espera explícita para esperar la visibilidad del elemento
            wait_action = ExplicitWaitAction(self.driver)
            wait_response = wait_action.execute(element_type, selector_value, condition="visibility", timeout=timeout)

            if wait_response['status'] == 'fail':
                return wait_response

            # Obtener el elemento select
            element = self.get_element(element_type, selector_value)
            select_element = Select(element)

            # Capturar todas las opciones disponibles
            available_options = [option.text for option in select_element.options]

            # Intentar seleccionar por texto visible o por valor
            if input_value:
                try:
                    select_element.select_by_visible_text(input_value)
                except NoSuchElementException:
                    try:
                        # Intentar seleccionar por valor si no se encuentra por texto visible
                        select_element.select_by_value(input_value)
                    except NoSuchElementException:
                        return self.default_response(
                            action='select',
                            element=selector_value,
                            status='fail',
                            error=f"No se encontró la opción '{input_value}'",
                            available_options=available_options
                        )

                # Si la selección fue exitosa
                return self.default_response(
                    action='select',
                    element=selector_value,
                    status='success',
                    input_value=input_value,
                    available_options=available_options
                )
            else:
                # Si no se proporcionó 'input_value'
                return self.default_response(
                    action='select',
                    element=selector_value,
                    status='fail',
                    error="No se proporcionó 'input_value'.",
                    available_options=available_options
                )
        
        except TimeoutException:
            return self.default_response(
                action='select',
                element=selector_value,
                status='fail',
                error=f"Timeout al esperar el elemento '{selector_value}'"
            )
        
        except ElementNotInteractableException:
            return self.default_response(
                action='select',
                element=selector_value,
                status='fail',
                error="El elemento no es interactuable."
            )
        
        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='select',
                element=selector_value,
                status='fail',
                error=str(e),
                available_options=available_options
            )
