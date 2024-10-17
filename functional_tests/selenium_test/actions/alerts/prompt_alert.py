from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_test.selenium_test.base_action import BaseAction
import time

class PromptAlertAction(BaseAction):
    def __init__(self, driver):
        super().__init__(driver)
            
    def execute(self, prompt_text=None):
        try:
            # Esperar que la alerta de tipo prompt esté presente (máximo 10 segundos)
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert  # Cambiar el foco a la alerta

            if prompt_text:
                alert.send_keys(prompt_text)  # Ingresar el texto en el cuadro de diálogo prompt

            alert.accept()  # Aceptar el prompt
            
            # Opcional: Agregar una breve pausa para asegurar que la alerta se procese correctamente
            time.sleep(0.5)  # Esto es útil si ves problemas de sincronización, ajusta el tiempo según sea necesario
            
            # Retornar una respuesta estándar de éxito
            return self.default_response(action="prompt_alert", element="alert", status="success", prompt_text=prompt_text)
        
        except TimeoutException:
            # Manejar el caso en que la alerta no apareció en el tiempo esperado
            return self.default_response(
                action="prompt_alert", 
                element="alert", 
                status="fail", 
                error="TimeoutException: No se encontró ningún cuadro de diálogo prompt después de 10 segundos."
            )
        
        except NoAlertPresentException:
            # Manejar el caso en que no hay ninguna alerta presente cuando se esperaba un prompt
            return self.default_response(
                action="prompt_alert", 
                element="alert", 
                status="fail", 
                error="NoAlertPresentException: No se encontró ningún cuadro de diálogo prompt."
            )
        
        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action="prompt_alert", 
                element="alert", 
                status="fail", 
                error=f"Error inesperado: {str(e)}"
            )
