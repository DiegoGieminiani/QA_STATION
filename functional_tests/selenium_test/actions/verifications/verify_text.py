from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction
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

            # Obtener el valor real del campo
            actual_value = element.get_attribute("value")

            # Si no hay 'value', obtenemos el 'text'
            if actual_value is None or actual_value.strip() == '':
                actual_value = element.text

            # Verificar si actual_value sigue siendo None antes de continuar
            if actual_value is None:
                return self.default_response(
                    action='verify_text',
                    element=selector_value,
                    status='fail',
                    error="Element text or value is None."
                )

            # Normalizar los valores eliminando saltos de línea y espacios extra
            actual_value_clean = actual_value.replace('\n', ' ').strip()
            expected_value_clean = expected_value.replace('\n', ' ').strip()

            # Comparación flexible: verificar si el valor esperado está en el valor real
            if expected_value_clean in actual_value_clean:
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
