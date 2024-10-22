
from functional_tests.selenium_test.base_action import BaseAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    ElementClickInterceptedException, 
    NoSuchElementException, 
    StaleElementReferenceException
)
from functional_tests.selenium_test.base_action import BaseAction

class ClickAction(BaseAction):
    def log_message(self, message):
        """Método para registrar mensajes en el log."""
        print(f"LOG: {message}")
        
    def execute(self, element_type, selector_value, timeout=10, retries=3, **kwargs):
        try:
            if not element_type or not selector_value:
                return self.default_response(
                    action='click',
                    element=selector_value,
                    status='fail',
                    error="Parámetros inválidos: 'element_type' o 'selector_value' no pueden ser nulos."
                )

            by_type, selector = self.get_by_type(element_type, selector_value)

            # Reintentos si el clic falla
            for attempt in range(retries):
                try:
                    # Esperar a que el elemento esté presente y visible
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((by_type, selector))
                    )

                    # Desplazar si no es visible
                    if not element.is_displayed():
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                        WebDriverWait(self.driver, timeout).until(EC.visibility_of(element))

                    # Verificar si es clickeable y hacer clic con JavaScript si es necesario
                    WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by_type, selector)))
                    try:
                        element.click()
                    except ElementClickInterceptedException:
                        self.log_message("El clic fue interceptado. Intentando con JavaScript.")
                        self.driver.execute_script("arguments[0].click();", element)

                    return self.default_response(
                        action='click',
                        element=selector_value,
                        status='success'
                    )

                except (ElementClickInterceptedException, StaleElementReferenceException) as e:
                    self.log_message(f"Intento {attempt + 1} fallido. Error: {str(e)}")
                    if attempt < retries - 1:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    else:
                        raise e

            return self.default_response(
                action='click',
                element=selector_value,
                status='fail',
                error=f"No se pudo hacer clic en el elemento tras {retries} intentos."
            )

        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            return self.default_response(
                action='click',
                element=selector_value,
                status='fail',
                error=str(e)
            )

        except Exception as e:
            return self.default_response(
                action='click',
                element=selector_value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
