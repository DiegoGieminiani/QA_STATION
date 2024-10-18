from functional_tests.selenium_test.base_action import BaseAction
from selenium.common.exceptions import NoSuchElementException, JavascriptException

class ScrollIntoViewAction(BaseAction):
    def execute(self, driver, locator, value):
        try:
            # Validar que los parámetros no sean nulos o vacíos
            if not locator or not value:
                return self.default_response(
                    action='scroll_into_view',
                    element=value,
                    status='fail',
                    error="Parámetros inválidos: 'locator' o 'value' no pueden ser nulos."
                )

            # Encontrar el elemento
            element = driver.find_element(locator, value)

            # Ejecutar la acción de scroll
            driver.execute_script("arguments[0].scrollIntoView(true);", element)

            # Devolver una respuesta exitosa
            return self.default_response(
                action='scroll_into_view',
                element=value,
                status='success'
            )

        except NoSuchElementException:
            # Manejar si el elemento no es encontrado
            return self.default_response(
                action='scroll_into_view',
                element=value,
                status='fail',
                error=f"No se encontró el elemento con el locator: {locator} y valor: {value}"
            )

        except JavascriptException as e:
            # Manejar cualquier error de JavaScript
            return self.default_response(
                action='scroll_into_view',
                element=value,
                status='fail',
                error=f"Error de JavaScript al hacer scroll al elemento: {str(e)}"
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='scroll_into_view',
                element=value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
