from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction
from selenium.common.exceptions import TimeoutException

class WaitForTextAction(BaseAction):
    def execute(self, element_type, selector_value, expected_text, timeout=10, **kwargs):
        try:
            # Esperar hasta que el texto esperado esté presente en el elemento
            WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element((self.get_by_type(element_type, selector_value)), expected_text))

            # Retornar éxito si el texto es encontrado
            return self.default_response(action="wait_for_text", element=selector_value, status="success", expected_text=expected_text)

        except TimeoutException:
            return self.default_response(action="wait_for_text", element=selector_value, status="fail", error="Timeout: No se encontró el texto en el tiempo esperado.")
        except Exception as e:
            return self.default_response(action="wait_for_text", element=selector_value, status="fail", error=str(e))
