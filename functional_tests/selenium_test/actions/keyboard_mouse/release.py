from functional_test.selenium_test.base_action import BaseAction
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

class ReleaseAction(BaseAction):
    def execute(self, **kwargs):
        try:
            # Crear la acción de release
            actions = ActionChains(self.driver)
            actions.release().perform()

            # Retornar la respuesta estándar de éxito
            return self.default_response(
                action='release',
                element=None,  # No se requiere un elemento específico
                status='success'
            )

        except NoSuchElementException:
            return self.default_response(
                action='release',
                element=None,
                status='fail',
                error="No se pudo realizar el release porque no se encontró el elemento."
            )

        except ElementNotInteractableException:
            return self.default_response(
                action='release',
                element=None,
                status='fail',
                error="No se pudo interactuar con el elemento para realizar el release."
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='release',
                element=None,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
