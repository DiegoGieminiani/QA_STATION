from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction

class ConfirmAlertAction(BaseAction):
    def __init__(self, driver):
        super().__init__(driver)
    
    def execute(self, accept=True):
        try:
            # Esperar que la alerta esté presente (máximo 10 segundos)
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert  # Cambiar el foco a la alerta

            if accept:
                alert.accept()  # Aceptar la confirmación
            else:
                alert.dismiss()  # Cancelar la confirmación

            # Retornar una respuesta estándar de éxito con el estado de aceptación/cancelación
            return self.default_response(action="confirm_alert", element="alert", status="success", accepted=accept)
        
        except TimeoutException:
            # Manejar el caso en que la alerta no aparezca dentro de los 10 segundos de espera
            return self.default_response(
                action="confirm_alert", 
                element="alert", 
                status="fail", 
                error="TimeoutException: No se encontró ninguna confirmación en el tiempo esperado."
            )
        
        except NoAlertPresentException:
            # Manejar el caso en que no hay ninguna alerta de confirmación presente
            return self.default_response(
                action="confirm_alert", 
                element="alert", 
                status="fail", 
                error="NoAlertPresentException: No se encontró ninguna confirmación para aceptar o cancelar."
            )
        
        except Exception as e:
            # Capturar cualquier otro tipo de excepción y devolver el error específico
            return self.default_response(
                action="confirm_alert", 
                element="alert", 
                status="fail", 
                error=f"Error inesperado: {str(e)}"
            )
