from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
import time  # Para el delay controlado

class BaseAction:
    def __init__(self, driver):
        self.driver = driver

    def get_by_type(self, element_type, selector_value):
        # Mapeo de los tipos de localizadores de Selenium
        by_types = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css_selector": By.CSS_SELECTOR,
            "class_name": By.CLASS_NAME,
            "tag_name": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT
        }
        
        by_type = by_types.get(element_type.lower())
        if not by_type:
            raise ValueError(f"Tipo de selector '{element_type}' no soportado.")
        
        return by_type, selector_value

    def handle_exceptions(self, exception, element_type=None, selector_value=None):
        """
        Método centralizado para manejar excepciones de Selenium.
        """
        if isinstance(exception, TimeoutException):
            message = f"Tiempo de espera agotado para el elemento '{selector_value}' con tipo '{element_type}'."
        elif isinstance(exception, NoSuchElementException):
            message = f"El elemento '{selector_value}' no se pudo encontrar usando '{element_type}'."
        elif isinstance(exception, ElementClickInterceptedException):
            message = f"No se pudo hacer clic en el elemento '{selector_value}' con tipo '{element_type}'."
        else:
            message = f"Ocurrió un error inesperado: {str(exception)}"
        
        print(message)
        raise exception  # Volvemos a lanzar la excepción para que el flujo la maneje

    def get_element(self, element_type, selector_value, timeout=30, check_visibility=True, check_clickable=False):
        """
        Método para obtener un elemento dado su tipo y selector, con manejo de tiempo de espera.
        Puede opcionalmente verificar si el elemento es visible o clickeable.
        """
        try:
            by_type, selector = self.get_by_type(element_type, selector_value)
            
            if check_clickable:
                # Verificar si el elemento es clickeable
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((by_type, selector))
                )
            elif check_visibility:
                # Verificar si el elemento es visible
                element = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((by_type, selector))
                )
            else:
                # Verificar si el elemento está presente en el DOM
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by_type, selector))
                )
            
            # Desplazar el elemento a la vista
            self.scroll_into_view(element)

            # Añadir un pequeño delay controlado para garantizar que sea interactuable
            time.sleep(1)
            
            return element

        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            # Manejar las excepciones con el método centralizado y volver a lanzarlas
            self.handle_exceptions(e, element_type, selector_value)
        except Exception as e:
            # Cualquier otro tipo de error
            self.handle_exceptions(e)

    def wait_for_condition(self, condition, element_type, selector_value, timeout=30):
        conditions_map = {
            "visibility": EC.visibility_of_element_located,
            "clickable": EC.element_to_be_clickable,
            "presence": EC.presence_of_element_located,
            "text_to_be_present": EC.text_to_be_present_in_element,
            "selected": EC.element_to_be_selected
        }

        try:
            by_type, selector = self.get_by_type(element_type, selector_value)
            selected_condition = conditions_map.get(condition)
            if not selected_condition:
                raise ValueError(f"Condición de espera '{condition}' no soportada.")
            
            # Aplicar la condición de espera seleccionada
            return WebDriverWait(self.driver, timeout).until(
                selected_condition((by_type, selector))
            )
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            # Manejar las excepciones con el método centralizado y volver a lanzarlas
            self.handle_exceptions(e, element_type, selector_value)
        except Exception as e:
            # Cualquier otro tipo de error
            self.handle_exceptions(e)

    def scroll_into_view(self, element):
        """
        Método para desplazar un elemento a la vista usando JavaScript.
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
            print("Elemento desplazado a la vista.")
        except Exception as e:
            print(f"Error al desplazar el elemento a la vista: {str(e)}")
            raise e


    def default_response(self, action, element, status="success", **extra):
        """
        Genera una respuesta estándar que puede ser extendida con más atributos.
        Si el estado es "fail", todo el test debe fallar.
        """
        response = {
            'action': action,
            'element': element,
            'status': status
        }
        
        # Si la acción falla, imprimir el error y permitir que el test falle
        if status == "fail":
            print(f"Test failed at action: {action}, element: {element}")
        
        response.update(extra)  # Permite agregar más atributos si es necesario
        return response
