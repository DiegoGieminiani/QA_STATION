from functional_test.selenium_test.base_action import BaseAction
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

class DragAndDropAction(BaseAction):
    def execute(self, source_type, source_selector, target_type, target_selector, **kwargs):
        try:
            # Obtener los elementos de origen y destino usando get_element
            source_element = self.get_element(source_type, source_selector)
            target_element = self.get_element(target_type, target_selector)

            # Crear una instancia de ActionChains para realizar la acción de arrastrar y soltar
            action_chains = ActionChains(self.driver)
            action_chains.drag_and_drop(source_element, target_element).perform()

            # Retornamos el resultado de éxito
            return self.default_response(action="drag_and_drop", element=source_selector, status="success", target=target_selector)

        except NoSuchElementException:
            return self.default_response(action="drag_and_drop", element=source_selector, status="fail", error="Elemento de origen o destino no encontrado.")
        except ElementNotInteractableException:
            return self.default_response(action="drag_and_drop", element=source_selector, status="fail", error="Elemento no es interactuable.")
        except Exception as e:
            return self.default_response(action="drag_and_drop", element=source_selector, status="fail", error=str(e))
