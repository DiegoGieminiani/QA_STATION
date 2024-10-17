from functional_test.selenium_test.base_action import BaseAction
from selenium.common.exceptions import NoSuchElementException, JavascriptException

class GetElementPropertyAction(BaseAction):
    def execute(self, driver, locator, value, property_name):
        try:
            # Validar que los parámetros no sean nulos o vacíos
            if not locator or not value or not property_name:
                return self.default_response(
                    action='get_element_property',
                    element=value,
                    status='fail',
                    error="Parámetros inválidos: 'locator', 'value' o 'property_name' no pueden ser nulos."
                )

            # Encontrar el elemento
            element = driver.find_element(locator, value)

            # Obtener la propiedad del elemento usando JavaScript
            property_value = driver.execute_script(f"return arguments[0].{property_name};", element)

            # Devolver el valor de la propiedad obtenida
            return self.default_response(
                action='get_element_property',
                element=value,
                status='success',
                property_name=property_name,
                property_value=property_value
            )

        except NoSuchElementException:
            # Manejar si el elemento no es encontrado
            return self.default_response(
                action='get_element_property',
                element=value,
                status='fail',
                error=f"No se encontró el elemento con el locator: {locator} y valor: {value}"
            )

        except JavascriptException as e:
            # Manejar cualquier error de ejecución de JavaScript
            return self.default_response(
                action='get_element_property',
                element=value,
                status='fail',
                error=f"Error de JavaScript al obtener la propiedad '{property_name}': {str(e)}"
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action='get_element_property',
                element=value,
                status='fail',
                error=f"Error inesperado: {str(e)}"
            )
