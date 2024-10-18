from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction
from selenium.common.exceptions import TimeoutException

class WaitForUrlAction(BaseAction):
    def execute(self, expected_url, timeout=10, **kwargs):
        try:
            # Esperar a que la URL cambie y coincida con la URL esperada
            WebDriverWait(self.driver, timeout).until(EC.url_to_be(expected_url))

            # Retornar éxito si la URL coincide
            return self.default_response(action="wait_for_url", element="URL", status="success", expected_url=expected_url)

        except TimeoutException:
            return self.default_response(action="wait_for_url", element="URL", status="fail", error="Timeout: La URL no coincidió a tiempo.")
        except Exception as e:
            return self.default_response(action="wait_for_url", element="URL", status="fail", error=str(e))
