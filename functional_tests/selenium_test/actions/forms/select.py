from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from functional_tests.selenium_test.base_action import BaseAction
from functional_tests.selenium_test.waits.explicit_wait import ExplicitWaitAction



class SelectAction(BaseAction):
    def execute(self, element_type, selector_value, input_value=None, timeout=10, **kwargs):
        try:
            # Esperar hasta que el elemento esté visible
            wait_action = ExplicitWaitAction(self.driver)
            wait_response = wait_action.execute(element_type, selector_value, condition="visibility", timeout=timeout)

            if wait_response['status'] == 'fail':
                return wait_response

            # Obtener el elemento select
            element = self.get_element(element_type, selector_value)

            # Verificar si el elemento es un dropdown estándar
            if element.tag_name == 'select':
                try:
                    select_element = Select(element)
                    select_element.select_by_visible_text(input_value)

                    return self.default_response(
                        action='select',
                        element=selector_value,
                        status='success',
                        input_value=input_value
                    )
                except NoSuchElementException:
                    return self.default_response(
                        action='select',
                        element=selector_value,
                        status='fail',
                        error=f"No se encontró la opción '{input_value}' en el <select>"
                    )
            else:
                # Si no es un <select>, usar JavaScript para abrir y seleccionar una opción
                print(f"Intentando seleccionar opción {input_value} en dropdown personalizado")
                self.driver.execute_script("arguments[0].click();", element)

                # Ajuste para dropdown personalizado, buscando cualquier etiqueta que contenga el texto
                option_xpath = f"//*[contains(text(), '{input_value}')]"
                try:
                    option = WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable((By.XPATH, option_xpath))
                    )
                    self.driver.execute_script("arguments[0].click();", option)

                    return self.default_response(
                        action='select',
                        element=selector_value,
                        status='success',
                        input_value=input_value
                    )
                except TimeoutException:
                    return self.default_response(
                        action='select',
                        element=selector_value,
                        status='fail',
                        error=f"Timeout al intentar seleccionar la opción '{input_value}'"
                    )

        except TimeoutException:
            return self.default_response(
                action='select',
                element=selector_value,
                status='fail',
                error=f"Timeout al hacer clic en '{selector_value}'"
            )

        except NoSuchElementException:
            return self.default_response(
                action='select',
                element=selector_value,
                status='fail',
                error=f"No se encontró la opción '{input_value}' o el elemento '{selector_value}'"
            )

        except ElementNotInteractableException:
            return self.default_response(
                action='select',
                element=selector_value,
                status='fail',
                error="El elemento no es interactuable."
            )

        except Exception as e:
            return self.default_response(
                action='select',
                element=selector_value,
                status='fail',
                error=str(e)
            )
