from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction
from selenium.webdriver.common.by import By

class VerifyElementHasChildWithClass(BaseAction):
    def execute(self, element_type, selector_value, child_class, timeout=15):
        try:
            by_type, selector = self.get_by_type(element_type, selector_value)
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_type, selector))
            )
            child_element = element.find_element(By.XPATH, f".//*[contains(@class, '{child_class}')]")
            
            if child_element:
                return self.default_response(action='verify_element_has_child', element=selector_value, status="success")
            else:
                return self.default_response(action='verify_element_has_child', element=selector_value, status="fail", error=f"El hijo con clase '{child_class}' no se encontró.")
        
        except TimeoutException:
            return self.default_response(action='verify_element_has_child', element=selector_value, status="fail", error="Timeout esperando el elemento.")
        
        except NoSuchElementException:
            return self.default_response(action='verify_element_has_child', element=selector_value, status="fail", error="Elemento o hijo no encontrado.")
