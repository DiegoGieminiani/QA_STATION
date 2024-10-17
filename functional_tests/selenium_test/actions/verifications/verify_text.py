from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_test.selenium_test.base_action import BaseAction
import re

class VerifyTextAction(BaseAction):
    def execute(self, element_type=None, selector_value=None, expected_value=None, timeout=15, **kwargs):
        try:
            if expected_value is None:
                return self.default_response(
                    action='verify_text',
                    element=selector_value,
                    status='fail',
                    error="'expected_value' cannot be null."
                )

            # Obtener el selector y valor
            by_type, selector = self.get_by_type(element_type, selector_value)

            # Esperar hasta que el elemento esté presente
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_type, selector))
            )

            # Obtener el valor real del campo (usando 'get_attribute' para casos 'readonly')
            actual_value = element.get_attribute("value").strip()

            # Si no hay 'value', intentamos obtener el 'text'
            if not actual_value:
                actual_value = element.text.strip()

            # Verificación robusta de tipos con 'if-elif'
            if isinstance(expected_value, (int, float)):
                # Comparación numérica
                try:
                    actual_value_num = float(actual_value)
                    expected_value_num = float(expected_value)
                    if actual_value_num == expected_value_num:
                        return self.default_response(
                            action='verify_text',
                            element=selector_value,
                            status='success',
                            actual_value=actual_value
                        )
                    else:
                        return self.default_response(
                            action='verify_text',
                            element=selector_value,
                            status='fail',
                            error=f"Expected number: {expected_value}, Actual number: {actual_value}"
                        )
                except ValueError:
                    # Si no se puede convertir a número, falla
                    return self.default_response(
                        action='verify_text',
                        element=selector_value,
                        status='fail',
                        error=f"Cannot convert actual value '{actual_value}' to a number."
                    )
            
            elif isinstance(expected_value, str):
                # Comparación de cadenas
                expected_value_clean = expected_value.strip()
                actual_value_clean = actual_value.strip()

                if actual_value_clean == expected_value_clean:
                    return self.default_response(
                        action='verify_text',
                        element=selector_value,
                        status='success',
                        actual_value=actual_value_clean
                    )
                else:
                    return self.default_response(
                        action='verify_text',
                        element=selector_value,
                        status='fail',
                        error=f"Expected text: '{expected_value_clean}', Actual text: '{actual_value_clean}'"
                    )

            elif isinstance(expected_value, list):
                # Comparación de listas (por ejemplo, opciones de dropdown)
                actual_values = actual_value.split(',')  # Supón que las opciones están separadas por coma
                if all(item in actual_values for item in expected_value):
                    return self.default_response(
                        action='verify_text',
                        element=selector_value,
                        status='success',
                        actual_value=actual_values
                    )
                else:
                    return self.default_response(
                        action='verify_text',
                        element=selector_value,
                        status='fail',
                        error=f"Expected list: {expected_value}, Actual list: {actual_values}"
                    )
            
            else:
                # Caso para otros tipos que podrían agregarse en el futuro
                return self.default_response(
                    action='verify_text',
                    element=selector_value,
                    status='fail',
                    error="Unsupported 'expected_value' type."
                )

        except TimeoutException:
            return self.default_response(
                action='verify_text',
                element=selector_value,
                status='fail',
                error="Timeout waiting for the element to be present."
            )

        except NoSuchElementException:
            return self.default_response(
                action='verify_text',
                element=selector_value,
                status='fail',
                error="Element not found."
            )

        except Exception as e:
            return self.default_response(
                action='verify_text',
                element=selector_value,
                status='fail',
                error=f"Unexpected error: {str(e)}"
            )
