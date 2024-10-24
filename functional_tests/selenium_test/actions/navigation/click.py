from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    ElementClickInterceptedException, 
    NoSuchElementException, 
    StaleElementReferenceException,
    ElementNotInteractableException
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from functional_tests.selenium_test.base_action import BaseAction
import logging

logging.basicConfig(level=logging.INFO)

class ClickAction(BaseAction):
    
    def log_message(self, message):
        """
        Método para registrar mensajes de log.
        Se puede modificar para registrar en un archivo, si es necesario.
        """
        logging.info(message)
    
    def execute(self, element_type, selector_value, retries=2, **kwargs):
        """
        Método principal que intentará todas las estrategias de clic de forma secuencial hasta encontrar la que funcione.
        Se probarán varias estrategias de clic: tradicional, ActionChains, JavaScript, y Enter key.
        """
        strategies = [
            self.click_traditional,
            self.click_with_action_chains,
            self.click_with_js,
            self.send_enter_key,
        ]

        for attempt in range(retries):
            try:
                # Obtener el elemento con un timeout de 20 segundos
                element = self.get_element(element_type, selector_value, timeout=20, check_visibility=True)
                
                # Intentar cada estrategia de clic en secuencia
                for strategy in strategies:
                    self.log_message(f"Intentando estrategia: {strategy.__name__}")
                    if strategy(element):
                        self.log_message(f"Estrategia {strategy.__name__} exitosa.")
                        return self.default_response(action='click', element=selector_value, status='success')

            except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
                # Manejo de excepciones comunes con logging
                self.log_message(f"Intento {attempt + 1} fallido. Error: {str(e)}")
                if attempt == retries - 1:
                    return self.default_response(action='click', element=selector_value, status='fail', error=str(e))

            except Exception as e:
                # Capturar cualquier otro error inesperado
                self.log_message(f"Error inesperado en el clic: {str(e)}")
                if attempt == retries - 1:
                    return self.default_response(action='click', element=selector_value, status='fail', error=str(e))

        # Retornar fail si todas las estrategias fallan
        return self.default_response(action='click', element=selector_value, status='fail', error="No se pudo hacer clic tras varios intentos.")

    def click_traditional(self, element):
        """Intentar clic tradicional."""
        try:
            element.click()
            self.log_message("Click tradicional realizado con éxito.")
            return True
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            self.log_message(f"Click tradicional fallido: {str(e)}")
            return False

    def click_with_action_chains(self, element):
        """Intentar clic usando ActionChains."""
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click().perform()
            self.log_message("Click con ActionChains realizado con éxito.")
            return True
        except Exception as e:
            self.log_message(f"Click con ActionChains fallido: {str(e)}")
            return False

    def click_with_js(self, element):
        """Intentar clic con JavaScript."""
        try:
            self.driver.execute_script("arguments[0].click();", element)
            self.log_message("Click con JavaScript realizado con éxito.")
            return True
        except Exception as e:
            self.log_message(f"Click con JavaScript fallido: {str(e)}")
            return False

    def send_enter_key(self, element):
        """Enviar la tecla Enter como alternativa al clic."""
        try:
            element.send_keys(Keys.RETURN)
            self.log_message("Tecla Enter enviada con éxito.")
            return True
        except Exception as e:
            self.log_message(f"Envío de tecla Enter fallido: {str(e)}")
            return False
