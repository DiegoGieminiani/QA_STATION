from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction

class VerifyUrlAction(BaseAction):
    
    def execute(self, expected_value=None, timeout=10, **kwargs):
        try:
            # Verificar que el expected_value esté presente
            if not expected_value:
                return self.default_response(
                    action='verify_url',
                    element='url',
                    status='fail',
                    error="Missing 'expected_value' for URL verification."
                )

            # Esperar hasta que la URL actual sea estable o se alcance el timeout
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.current_url != ""
            )

            # Obtener la URL actual
            current_url = self.driver.current_url
            print(f"[DEBUG] Actual URL: {current_url}")
            print(f"[DEBUG] Expected URL: {expected_value}")

            # Normalizar ambas URLs eliminando el slash final
            normalized_current_url = current_url.rstrip('/')
            normalized_expected_url = expected_value.rstrip('/')

            print(f"[DEBUG] Normalized Current URL: {normalized_current_url}")
            print(f"[DEBUG] Normalized Expected URL: {normalized_expected_url}")

            # Comprobar si la URL actual coincide con la esperada
            if normalized_current_url == normalized_expected_url:
                return self.default_response(
                    action='verify_url',
                    element='url',
                    status='success',
                    verified_value=current_url
                )
            else:
                return self.default_response(
                    action='verify_url',
                    element='url',
                    status='fail',
                    error=f"URLs are different! Expected: {expected_value}, but got: {current_url}"
                )

        except TimeoutException:
            return self.default_response(
                action='verify_url',
                element='url',
                status='fail',
                error=f"Timeout waiting for the URL to match '{expected_value}'."
            )

        except Exception as e:
            return self.default_response(
                action='verify_url',
                element='url',
                status='fail',
                error=f"Unexpected error verifying URL: {str(e)}"
            )
