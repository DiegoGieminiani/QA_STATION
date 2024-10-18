from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from functional_tests.selenium_test.base_action import BaseAction

class ClickAction(BaseAction):
    def execute(self, element_type, selector_value, timeout=10, **kwargs):
        try:
            # Validar parámetros
            if not element_type or not selector_value:
                return self.default_response(
                    action='click',
                    element=selector_value,
                    status='fail',
                    error="Parámetros inválidos: 'element_type' o 'selector_value' no pueden ser nulos."
                )

            # Obtener el tipo de localizador y el selector
            by_type, selector = self.get_by_type(element_type, selector_value)

            # Obtener el elemento con espera
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_type, selector))
            )

            # Desplazar si no es visible
            if not element.is_displayed():
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                WebDriverWait(self.driver, timeout).until(EC.visibility_of(element))

            # Esperar a que sea clicable
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by_type, selector)))

            # Intentar clic con Selenium
            try:
                element.click()
            except ElementClickInterceptedException:
                # Clic con JavaScript si falla
                self.driver.execute_script("arguments[0].click();", element)

            # Respuesta de éxito
            return self.default_response(
                action='click',
                element=selector_value,
                status='success'
            )

        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            # Manejo de errores comunes
            return self.default_response(
                action='click',
                element=selector_value,
                status='fail',
                error=str(e)
            )

        except Exception as e:
            # Manejo de errores inesperados
            return self.default_response(
                action='click',
                element=selector_value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
