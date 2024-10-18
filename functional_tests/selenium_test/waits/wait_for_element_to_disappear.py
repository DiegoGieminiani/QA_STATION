from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction
from selenium.common.exceptions import TimeoutException

class WaitForElementToDisappearAction(BaseAction):
    def execute(self, element_type, selector_value, timeout=10, **kwargs):
        try:
            # Esperar hasta que el elemento desaparezca (no sea visible)
            self.wait_for_condition(EC.invisibility_of_element_located, element_type, selector_value, timeout)

            # Retornar éxito si el elemento desaparece
            return self.default_response(action="wait_for_element_to_disappear", element=selector_value, status="success")

        except TimeoutException:
            return self.default_response(action="wait_for_element_to_disappear", element=selector_value, status="fail", error="Timeout: El elemento no desapareció a tiempo.")
        except Exception as e:
            return self.default_response(action="wait_for_element_to_disappear", element=selector_value, status="fail", error=str(e))
