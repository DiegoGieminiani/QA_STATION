from functional_tests.selenium_test.base_action import BaseAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class ExtractListItemsAction(BaseAction):
    def execute(self, driver, locator, value):
        try:
            # Validar si el locator y el value no son vacíos
            if not locator or not value:
                return self.default_response(action="extract_list_items", element=value, status="fail", error="El localizador o el valor del elemento no son válidos.")
            
            # Esperar hasta que los elementos estén presentes
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((locator, value)))

            # Encontrar los elementos de la lista
            elements = driver.find_elements(locator, value)
            
            # Extraer el texto de los elementos
            list_items = [element.text for element in elements if element.text]

            # Verificar si se encontraron elementos con texto
            if list_items:
                return self.default_response(action="extract_list_items", element=value, status="success", items=list_items)
            else:
                return self.default_response(action="extract_list_items", element=value, status="fail", error="No se encontraron elementos de lista con texto.")
        
        except TimeoutException:
            # Manejar el caso en que los elementos no aparecen dentro del tiempo esperado
            return self.default_response(action="extract_list_items", element=value, status="fail", error="TimeoutException: No se encontraron los elementos de lista en el tiempo esperado.")

        except NoSuchElementException:
            # Manejar el caso en que no se encuentran elementos
            return self.default_response(action="extract_list_items", element=value, status="fail", error=f"NoSuchElementException: No se encontraron elementos con {locator}='{value}'.")

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(action="extract_list_items", element=value, status="fail", error=f"Error inesperado: {str(e)}")
