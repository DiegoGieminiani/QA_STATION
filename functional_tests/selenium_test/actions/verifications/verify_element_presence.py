from functional_tests.selenium_test.base_action import BaseAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class VerifyElementPresence(BaseAction):
    def execute(self, element_type, selector_value, check_absence=False, check_enabled=False, timeout=15):
        try:
            by_type, selector = self.get_by_type(element_type, selector_value)
            
            if check_absence:
                # Verifica si el elemento NO está presente
                WebDriverWait(self.driver, timeout).until_not(
                    EC.presence_of_element_located((by_type, selector))
                )
                return self.default_response(action='verify_element_absence', element=selector_value, status="success")
                
            elif check_enabled:
                # Verifica si el elemento está habilitado (clickeable)
                WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((by_type, selector))
                )
                return self.default_response(action='verify_element_enabled', element=selector_value, status="success")
                
            else:
                # Verifica si el elemento está presente
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by_type, selector))
                )
                return self.default_response(action='verify_element_presence', element=selector_value, status="success")
            
        except TimeoutException:
            return self.default_response(action='verify_element_presence', element=selector_value, status="fail", error="Timeout esperando el elemento.")
        
        except NoSuchElementException:
            return self.default_response(action='verify_element_presence', element=selector_value, status="fail", error="Elemento no encontrado.")
