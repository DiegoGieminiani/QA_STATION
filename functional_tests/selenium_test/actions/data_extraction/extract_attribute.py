from functional_tests.selenium_test.base_action import BaseAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSelectorException

class ExtractAttributeAction(BaseAction):
    def execute(self, driver, locator, value, attribute):
        try:
            # Validar si el locator y el value no son vacíos
            if not locator or not value:
                return self.default_response(action="extract_attribute", element=value, status="fail", error="El localizador o el valor del elemento no son válidos.")

            # Esperar hasta que el elemento esté presente y sea visible
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((locator, value)))

            # Encontrar el elemento en la página web
            element = driver.find_element(locator, value)
            
            # Obtener el valor del atributo especificado
            attribute_value = element.get_attribute(attribute)
            
            # Verificar si el atributo fue encontrado y no es None
            if attribute_value is not None:
                # Retornar una respuesta estándar de éxito
                return self.default_response(
                    action="extract_attribute", 
                    element=value, 
                    status="success", 
                    attribute=attribute, 
                    attribute_value=attribute_value
                )
            else:
                # Manejar el caso en que el atributo no está presente en el elemento
                return self.default_response(
                    action="extract_attribute", 
                    element=value, 
                    status="fail", 
                    error=f"El atributo '{attribute}' no está presente en el elemento."
                )

        except InvalidSelectorException:
            # Manejar el caso en que el locator es inválido (ej. malformado)
            return self.default_response(
                action="extract_attribute", 
                element=value, 
                status="fail", 
                error="InvalidSelectorException: El localizador proporcionado es inválido o malformado."
            )
        
        except TimeoutException:
            # Manejar el caso en que el elemento no aparece dentro del tiempo esperado
            return self.default_response(
                action="extract_attribute", 
                element=value, 
                status="fail", 
                error="TimeoutException: No se encontró el elemento para extraer el atributo."
            )

        except NoSuchElementException:
            # Manejar el caso en que el elemento no se encuentra en la página
            return self.default_response(
                action="extract_attribute", 
                element=value, 
                status="fail", 
                error=f"NoSuchElementException: No se pudo encontrar el elemento con {locator}='{value}'."
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(
                action="extract_attribute", 
                element=value, 
                status="fail", 
                error=f"Error inesperado: {str(e)}"
            )
