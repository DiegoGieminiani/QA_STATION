from functional_test.selenium_test.base_action import BaseAction
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedTagNameException
from selenium.webdriver.support import expected_conditions as EC

class ExtractDropdownOptionsAction(BaseAction):
    def execute(self, driver, locator, value):
        try:
            # Validar si el locator y el value no son vacíos
            if not locator or not value:
                return self.default_response(action="extract_dropdown_options", element=value, status="fail", error="El localizador o el valor del elemento no son válidos.")

            # Esperar hasta que el elemento <select> esté presente
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((locator, value)))

            # Encontrar el elemento select
            dropdown = Select(driver.find_element(locator, value))

            # Extraer las opciones del dropdown y sus textos
            options = [option.text for option in dropdown.options]
            
            # Retornar una respuesta estándar con éxito
            return self.default_response(action="extract_dropdown_options", element=value, status="success", options=options)

        except TimeoutException:
            # Manejar el caso en que el elemento <select> no aparece dentro del tiempo esperado
            return self.default_response(action="extract_dropdown_options", element=value, status="fail", error="TimeoutException: No se encontró el elemento <select> en el tiempo esperado.")

        except NoSuchElementException:
            # Manejar el caso en que el elemento no se encuentra
            return self.default_response(action="extract_dropdown_options", element=value, status="fail", error=f"NoSuchElementException: No se pudo encontrar el elemento <select> con {locator}='{value}'.")

        except UnexpectedTagNameException:
            # Manejar el caso en que el elemento encontrado no es un <select>
            return self.default_response(action="extract_dropdown_options", element=value, status="fail", error=f"UnexpectedTagNameException: El elemento con {locator}='{value}' no es un <select>.")

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(action="extract_dropdown_options", element=value, status="fail", error=f"Error inesperado: {str(e)}")
