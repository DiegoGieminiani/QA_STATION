from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from functional_tests.selenium_test.base_action import BaseAction

class ExplicitWaitAction(BaseAction):
    def execute(self, element_type, selector_value, condition="visibility", timeout=10, **kwargs):
        try:
            # Definimos las condiciones de espera explícita disponibles
            conditions = {
                "visibility": EC.visibility_of_element_located,
                "clickable": EC.element_to_be_clickable,
                "presence": EC.presence_of_element_located,
                "invisibility": EC.invisibility_of_element_located
            }

            # Verificamos si la condición pasada es válida
            if condition not in conditions:
                raise ValueError(f"Condición '{condition}' no es válida. Usa 'visibility', 'clickable', 'presence', o 'invisibility'.")

            # Usamos el método wait para aplicar la espera basada en la condición seleccionada
            WebDriverWait(self.driver, timeout).until(conditions[condition]((self.get_by_type(element_type, selector_value))))

            # Retornamos éxito
            return self.default_response(action="explicit_wait", element=selector_value, status="success")

        except TimeoutException:
            return self.default_response(action="explicit_wait", element=selector_value, status="fail", error="Timeout: La condición no se cumplió a tiempo.")
        except Exception as e:
            return self.default_response(action="explicit_wait", element=selector_value, status="fail", error=str(e))
