from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction

class DismissAlertAction(BaseAction):
    def __init__(self, driver):
        super().__init__(driver)
        
    def execute(self):
        try:
            # Esperar hasta que la alerta esté presente
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.dismiss()

            # Retornar el resultado estándar de éxito
            return self.default_response(action='dismiss_alert', element='alert', status="success")
        
        except TimeoutException:
            return self.default_response(action='dismiss_alert', element='alert', status="fail", error="TimeoutException: No se encontró ninguna alerta para rechazar.")
        
        except NoAlertPresentException:
            return self.default_response(action='dismiss_alert', element='alert', status="fail", error="NoAlertPresentException: No se encontró ninguna alerta para rechazar.")

        except Exception as e:
            return self.default_response(action='dismiss_alert', element='alert', status="fail", error=str(e))
