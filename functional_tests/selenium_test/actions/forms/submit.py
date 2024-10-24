from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_tests.selenium_test.base_action import BaseAction

class SubmitFormAction(BaseAction):
    def execute(self, element_type, selector_value, **kwargs):
        try:
            # Validar que los parámetros no sean nulos
            if not element_type or not selector_value:
                return self.default_response(
                    action='submit_form',
                    element=selector_value,
                    status='fail',
                    error="Parámetros inválidos: 'element_type' o 'selector_value' no pueden ser nulos."
                )

            # Timeout configurable
            timeout = kwargs.get('timeout', 10)

            # Verificar si es un formulario estándar o un formulario modal basado en el tipo de elemento
            if element_type == 'form':
                # Formularios estándar: usar submit() directamente
                form = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(self.get_by_type(element_type, selector_value))
                )
                form.submit()  # Enviar formulario estándar

            else:
                # Formularios modales: hacer clic en el botón de envío
                submit_button = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(self.get_by_type(element_type, selector_value))
                )
                submit_button.click()  # Enviar mediante botón

            # Retornar la respuesta estándar de éxito
            return self.default_response(
                action='submit_form',
                element=selector_value,
                status='success',
                message="Formulario enviado con éxito."
            )

        except TimeoutException:
            return self.default_response(
                action='submit_form',
                element=selector_value,
                status='fail',
                error=f"Timeout esperando el elemento '{selector_value}'."
            )

        except NoSuchElementException:
            return self.default_response(
                action='submit_form',
                element=selector_value,
                status='fail',
                error="No se encontró el formulario o botón de envío."
            )

        except ElementNotInteractableException:
            return self.default_response(
                action='submit_form',
                element=selector_value,
                status='fail',
                error="El formulario o botón de envío no es interactuable."
            )

        except ElementClickInterceptedException:
            return self.default_response(
                action='submit_form',
                element=selector_value,
                status='fail',
                error="No se pudo hacer clic en el botón de envío del formulario modal."
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='submit_form',
                element=selector_value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
