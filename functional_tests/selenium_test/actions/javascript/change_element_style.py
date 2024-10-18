from functional_tests.selenium_test.base_action import BaseAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException

class ChangeElementStyleAction(BaseAction):
    def execute(self, driver, locator, value, style):
        try:
            # Validar que los parámetros sean válidos
            if not locator or not value or not style:
                return self.default_response(
                    action='change_element_style',
                    element=value,
                    status='fail',
                    error="Parámetros inválidos: 'locator', 'value' o 'style' no pueden ser nulos."
                )

            # Intentar encontrar el elemento
            element = driver.find_element(locator, value)

            # Cambiar el estilo del elemento
            driver.execute_script(f"arguments[0].style = '{style}';", element)

            # Devolver respuesta exitosa
            return self.default_response(
                action='change_element_style',
                element=value,
                status='success',
                style_applied=style
            )
        
        except NoSuchElementException:
            # Manejar si el elemento no es encontrado
            return self.default_response(
                action='change_element_style',
                element=value,
                status='fail',
                error=f"No se pudo encontrar el elemento con el locator: {locator} y valor: {value}"
            )

        except ElementNotInteractableException:
            # Manejar si el elemento no es interactuable
            return self.default_response(
                action='change_element_style',
                element=value,
                status='fail',
                error=f"El elemento no es interactuable para aplicar el estilo: {style}"
            )

        except TimeoutException:
            # Manejar timeout
            return self.default_response(
                action='change_element_style',
                element=value,
                status='fail',
                error=f"Timeout al intentar encontrar el elemento con locator: {locator}"
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='change_element_style',
                element=value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
