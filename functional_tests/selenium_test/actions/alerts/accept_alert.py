from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction
from functional_tests.selenium_test.screenshots.take_screenshots import take_screenshot
 # Asegúrate de importar la función

class AcceptAlertAction(BaseAction):
    def __init__(self, driver):
        super().__init__(driver)

    def execute(self, **kwargs):
        input_value = kwargs.get("input_value", None)  # Obtener valor para ingresar en la alerta, si es necesario
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            
            if input_value:  # Si hay un valor proporcionado, se ingresa en la alerta tipo prompt
                alert.send_keys(input_value)
            
            alert.accept()  # Aceptar la alerta
            
            # Tomar screenshot después de aceptar la alerta
            screenshot_path = take_screenshot(self.driver, "accept_alert", delay=2)
            
            return self.default_response(
                action='accept_alert', 
                element='alert', 
                status="success",
                screenshot=screenshot_path  # Añadir la ruta del screenshot al resultado
            )

        except TimeoutException:
            # Capturar pantalla si falla por Timeout
            screenshot_path = take_screenshot(self.driver, "accept_alert_timeout")
            return self.default_response(
                action='accept_alert', 
                element='alert', 
                status="fail", 
                error="Timeout: No se encontró la alerta.",
                screenshot=screenshot_path  # Añadir la captura
            )

        except NoAlertPresentException:
            # Capturar pantalla si no se encuentra la alerta
            screenshot_path = take_screenshot(self.driver, "accept_alert_no_alert")
            return self.default_response(
                action='accept_alert', 
                element='alert', 
                status="fail", 
                error="NoAlert: No se encontró la alerta.",
                screenshot=screenshot_path  # Añadir la captura
            )

        except Exception as e:
            # Capturar pantalla para cualquier otra excepción
            screenshot_path = take_screenshot(self.driver, "accept_alert_error")
            return self.default_response(
                action='accept_alert', 
                element='alert', 
                status="fail", 
                error=str(e),
                screenshot=screenshot_path  # Añadir la captura
            )
