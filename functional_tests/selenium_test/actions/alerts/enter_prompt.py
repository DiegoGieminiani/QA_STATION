from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_test.selenium_test.base_action import BaseAction
import time

class EnterPromptAction(BaseAction):
    def __init__(self, driver):
        super().__init__(driver)
        
    def execute(self, **kwargs):
        input_value = kwargs.get('input_value', None)  # Obtener input_value o dejarlo en None
        
        if input_value is None:
            return self.default_response(action="enter_prompt", element="alert", status="fail", error="input_value es obligatorio.")
        
        try:
            # Intentar esperar la alerta con tiempo de espera estándar (10 segundos)
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
        
        except NoAlertPresentException:
            # Si no aparece la alerta, forzarla usando execute_script
            try:
                self.driver.execute_script("window.alert('Triggered alert');")
                WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
            except NoAlertPresentException:
                return self.default_response(action="enter_prompt", element="alert", status="fail", error="NoAlertPresentException: No se pudo generar una alerta.")

        except TimeoutException:
            return self.default_response(action="enter_prompt", element="alert", status="fail", error="TimeoutException: No se encontró ninguna alerta prompt.")

        try:
            # Enviar el texto al cuadro de diálogo y aceptar la alerta
            alert.send_keys(input_value)
            alert.accept()

            # Retornar una respuesta de éxito
            return self.default_response(action="enter_prompt", element="alert", status="success", input_value=input_value)

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(action="enter_prompt", element="alert", status="fail", error=f"Error inesperado: {str(e)}")
