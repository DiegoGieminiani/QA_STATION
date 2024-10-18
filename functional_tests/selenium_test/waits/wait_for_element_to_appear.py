from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction
from selenium.common.exceptions import TimeoutException

class WaitForElementToAppearAction(BaseAction):
    def execute(self, element_type, selector_value, timeout=10, **kwargs):
        try:
            # Utilizar el método wait_for_condition de BaseAction para esperar la visibilidad del elemento
            self.wait_for_condition(EC.visibility_of_element_located, element_type, selector_value, timeout)

            # Retornar el resultado exitoso si el elemento es visible
            return self.default_response(action="wait_for_element_to_appear", element=selector_value, status="success")

        except TimeoutException:
            return self.default_response(action="wait_for_element_to_appear", element=selector_value, status="fail", error="Timeout: El elemento no apareció a tiempo.")
        except Exception as e:
            return self.default_response(action="wait_for_element_to_appear", element=selector_value, status="fail", error=str(e))
