from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from functional_test.selenium_test.base_action import BaseAction

class NavigateToUrlAction(BaseAction):
    def execute(self, url, **kwargs):
        try:
            # Validar que el URL no sea nulo o vacío
            if not url:
                return self.default_response(
                    action='navigate_to_url',
                    element='Navegador',
                    status='fail',
                    error="URL no proporcionado o inválido."
                )

            # Navegar a la URL proporcionada
            self.driver.get(url)

            # Retornar la respuesta estándar de éxito
            return self.default_response(
                action='navigate_to_url',
                element=url,
                status='success'
            )

        except NoSuchWindowException:
            return self.default_response(
                action='navigate_to_url',
                element=url,
                status='fail',
                error="No se pudo encontrar la ventana del navegador."
            )

        except TimeoutException:
            return self.default_response(
                action='navigate_to_url',
                element=url,
                status='fail',
                error="Timeout al intentar cargar la URL."
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='navigate_to_url',
                element=url,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
