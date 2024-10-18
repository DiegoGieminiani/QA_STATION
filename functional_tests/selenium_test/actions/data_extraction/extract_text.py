from functional_tests.selenium_test.base_action import BaseAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ExtractTextAction(BaseAction):
    def execute(self, element_type, selector_value, **kwargs):
        try:
            # Validar que el tipo de elemento y el valor del selector sean válidos
            if not element_type or not selector_value:
                return self.default_response(
                    action='extract_text', 
                    element=selector_value, 
                    status="fail", 
                    error="El tipo de elemento o el valor del selector no son válidos."
                )

            # Esperar hasta 30 segundos para que el elemento sea visible
            element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(self.get_by_type(element_type, selector_value))
            )
            
            # Desplazar el elemento al viewport en caso de que no esté visible
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            
            # Extraer el texto del elemento
            text = element.text.strip()  # Remover espacios innecesarios

            if not text:
                return self.default_response(
                    action='extract_text', 
                    element=selector_value, 
                    status="fail", 
                    error="El elemento se encontró, pero no contiene texto."
                )

            # Retornar el resultado si la extracción fue exitosa
            return self.default_response(
                action='extract_text', 
                element=selector_value, 
                status="success", 
                extracted_text=text
            )

        except TimeoutException:
            # Capturar TimeoutException y retornar un error detallado
            return self.default_response(
                action='extract_text', 
                element=selector_value, 
                status="fail", 
                error="Timeout esperando a que el elemento sea visible."
            )

        except NoSuchElementException:
            # Capturar NoSuchElementException en caso de que el selector esté incorrecto
            return self.default_response(
                action='extract_text', 
                element=selector_value, 
                status="fail", 
                error=f"El elemento no se encontró usando el selector: {selector_value}."
            )

        except Exception as e:
            # Captura de cualquier otra excepción inesperada
            return self.default_response(
                action='extract_text', 
                element=selector_value, 
                status="fail", 
                error=f"Error inesperado: {str(e)}"
            )
