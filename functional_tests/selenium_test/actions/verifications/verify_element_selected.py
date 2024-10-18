from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction

class VerifyElementSelected(BaseAction):
    def execute(self, element_type, selector_value, timeout=15, **kwargs):
        try:
            # Validar que los parámetros no sean nulos
            if not element_type or not selector_value:
                return self.default_response(
                    action='verify_element_selected',
                    element=selector_value,
                    status='fail',
                    error="Parámetros inválidos: 'element_type' o 'selector_value' no pueden ser nulos."
                )

            # Obtener el tipo de selector y el valor
            by_type, selector = self.get_by_type(element_type, selector_value)

            # Esperar hasta que el elemento sea clicable
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by_type, selector))
            )

            # Verificar si el elemento está seleccionado
            if element.is_selected():
                return self.default_response(
                    action='verify_element_selected',
                    element=selector_value,
                    status='success'
                )
            else:
                return self.default_response(
                    action='verify_element_selected',
                    element=selector_value,
                    status='fail',
                    error="El elemento no está seleccionado."
                )

        except TimeoutException:
            return self.default_response(
                action='verify_element_selected',
                element=selector_value,
                status='fail',
                error="Timeout esperando que el elemento esté presente y clicable."
            )

        except NoSuchElementException:
            return self.default_response(
                action='verify_element_selected',
                element=selector_value,
                status='fail',
                error="Elemento no encontrado."
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='verify_element_selected',
                element=selector_value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
