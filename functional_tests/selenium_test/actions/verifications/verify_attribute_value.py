from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction

class VerifyAttributeValue(BaseAction):
    def execute(self, element_type, selector_value, attribute, expected_value, timeout=15):
        try:
            by_type, selector = self.get_by_type(element_type, selector_value)
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_type, selector))
            )
            actual_value = element.get_attribute(attribute)
            
            if actual_value == expected_value:
                return self.default_response(action='verify_attribute_value', element=selector_value, status="success")
            else:
                return self.default_response(action='verify_attribute_value', element=selector_value, status="fail", 
                                             error=f"Expected: {expected_value}, Got: {actual_value}")
        except TimeoutException:
            return self.default_response(action='verify_attribute_value', element=selector_value, status="fail", error="Timeout esperando el elemento.")
        except NoSuchElementException:
            return self.default_response(action='verify_attribute_value', element=selector_value, status="fail", error="Elemento no encontrado.")
