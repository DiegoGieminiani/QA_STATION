from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException
from functional_tests.selenium_test.base_action import BaseAction

class ClickAndHoldAction(BaseAction):
    def __init__(self, driver):
        self.driver = driver

    def execute(self, locator, value, timeout=10):
        try:
            # Validar que los parámetros no sean nulos
            if not locator or not value:
                return self.default_response(
                    action='click_and_hold',
                    element=value,
                    status='fail',
                    error="Parámetros inválidos: 'locator' o 'value' no pueden ser nulos."
                )

            # Esperar a que el elemento esté disponible e interactuable
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((locator, value)))

            # Ejecutar la acción de click and hold
            actions = ActionChains(self.driver)
            actions.click_and_hold(element).perform()

            # Devolver una respuesta exitosa
            return self.default_response(
                action='click_and_hold',
                element=value,
                status='success'
            )

        except TimeoutException:
            # Manejar si el elemento no está disponible dentro del timeout
            return self.default_response(
                action='click_and_hold',
                element=value,
                status='fail',
                error=f"Timeout al esperar el elemento con locator: {locator} y valor: {value}"
            )

        except ElementNotInteractableException:
            # Manejar si el elemento no es interactuable
            return self.default_response(
                action='click_and_hold',
                element=value,
                status='fail',
                error=f"El elemento no es interactuable para la acción de click and hold."
            )

        except NoSuchElementException:
            # Manejar si no se encuentra el elemento
            return self.default_response(
                action='click_and_hold',
                element=value,
                status='fail',
                error=f"No se encontró el elemento con el locator: {locator} y valor: {value}"
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='click_and_hold',
                element=value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
