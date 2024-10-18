from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction

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
            return self.default_response(action='accept_alert', element='alert', status="success")

        except TimeoutException:
            return self.default_response(action='accept_alert', element='alert', status="fail", error="Timeout: No se encontró la alerta.")

        except NoAlertPresentException:
            return self.default_response(action='accept_alert', element='alert', status="fail", error="NoAlert: No se encontró la alerta.")

        except Exception as e:
            return self.default_response(action='accept_alert', element='alert', status="fail", error=str(e))


        except NoAlertPresentException:
            return self.default_response(action='accept_alert', element='alert', status="fail", error="No se encontró ninguna alerta para aceptar.")

        except Exception as e:
            return self.default_response(action='accept_alert', element='alert', status="fail", error=str(e))