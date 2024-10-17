from functional_test.selenium_test.base_action import BaseAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class ExtractLinksAction(BaseAction):
    def execute(self, driver, locator, value):
        try:
            # Validar si el locator y el value no son vacíos
            if not locator or not value:
                return self.default_response(action="extract_links", element=value, status="fail", error="El localizador o el valor del elemento no son válidos.")
            
            # Esperar hasta que los elementos estén presentes
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((locator, value)))

            # Encontrar los elementos que contienen enlaces
            elements = driver.find_elements(locator, value)
            
            # Extraer los enlaces (atributo href) de los elementos
            links = [element.get_attribute("href") for element in elements if element.get_attribute("href")]

            # Verificar si se encontraron enlaces
            if links:
                return self.default_response(action="extract_links", element=value, status="success", links=links)
            else:
                return self.default_response(action="extract_links", element=value, status="fail", error="No se encontraron enlaces (atributo 'href') en los elementos seleccionados.")
        
        except TimeoutException:
            # Manejar el caso en que los elementos no aparecen dentro del tiempo esperado
            return self.default_response(action="extract_links", element=value, status="fail", error="TimeoutException: No se encontraron los elementos con enlaces en el tiempo esperado.")

        except NoSuchElementException:
            # Manejar el caso en que no se encuentran elementos
            return self.default_response(action="extract_links", element=value, status="fail", error=f"NoSuchElementException: No se encontraron elementos con {locator}='{value}'.")

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(action="extract_links", element=value, status="fail", error=f"Error inesperado: {str(e)}")
