from functional_tests.selenium_test.base_action import BaseAction
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

class ScrollAction(BaseAction):
    def execute(self, x_offset=0, y_offset=500, **kwargs):
        """Desplaza la página hacia abajo o hacia arriba."""
        try:
            # Validar que los offsets sean números válidos
            if not isinstance(x_offset, (int, float)) or not isinstance(y_offset, (int, float)):
                return self.default_response(
                    action='scroll',
                    element=None,
                    status='fail',
                    error="Los valores de 'x_offset' y 'y_offset' deben ser numéricos."
                )

            # Ejecutar la acción de scroll
            self.driver.execute_script(f"window.scrollBy({x_offset}, {y_offset});")

            # Retornar una respuesta estándar de éxito
            return self.default_response(
                action='scroll',
                element=None,  # No se requiere un elemento específico
                status='success',
                x_offset=x_offset,
                y_offset=y_offset
            )

        except ElementNotInteractableException:
            # Manejar si la página no es interactuable
            return self.default_response(
                action='scroll',
                element=None,
                status='fail',
                error="La página no es interactuable para realizar el scroll."
            )

        except NoSuchElementException:
            # No se debería necesitar, ya que no estamos interactuando con un elemento
            return self.default_response(
                action='scroll',
                element=None,
                status='fail',
                error="No se pudo realizar el scroll debido a un error de elemento inexistente."
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='scroll',
                element=None,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
