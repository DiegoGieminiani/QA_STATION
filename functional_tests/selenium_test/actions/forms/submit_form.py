from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from functional_tests.selenium_test.base_action import BaseAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SubmitFormAction(BaseAction):
    def execute(self, driver, locator, **kwargs):
        try:
            # Validar si el locator es válido
            if not locator or len(locator) != 2:
                return self.default_response(
                    action='submit_form', 
                    element=locator, 
                    status="fail", 
                    error="El localizador del formulario no es válido."
                )
            
            # Timeout configurable, valor predeterminado de 10 segundos
            timeout = kwargs.get('timeout', 10)

            # Esperar hasta que el formulario esté presente y sea interactuable
            form = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((locator[0], locator[1]))
            )

            # Intentar enviar el formulario
            form.submit()

            # Respuesta de éxito
            return self.default_response(
                action='submit_form', 
                element=locator, 
                status="success", 
                message="Formulario enviado con éxito."
            )

        except TimeoutException:
            # Manejar el caso en que el formulario no está presente en el tiempo esperado
            return self.default_response(
                action='submit_form', 
                element=locator, 
                status="fail", 
                error="Timeout esperando al formulario."
            )
        
        except NoSuchElementException:
            # Manejar el caso en que no se encuentra el formulario
            return self.default_response(
                action='submit_form', 
                element=locator, 
                status="fail", 
                error="Formulario no encontrado."
            )
        
        except ElementNotInteractableException:
            # Manejar el caso en que el formulario no es interactuable
            return self.default_response(
                action='submit_form', 
                element=locator, 
                status="fail", 
                error="El formulario no es interactuable."
            )
        
        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='submit_form', 
                element=locator, 
                status="fail", 
                error=f"Error inesperado: {str(e)}"
            )
