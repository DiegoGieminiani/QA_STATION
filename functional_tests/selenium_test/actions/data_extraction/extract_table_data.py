from functional_tests.selenium_test.base_action import BaseAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class ExtractTableDataAction(BaseAction):
    def execute(self, driver, table_locator, row, column):
        try:
            # Validar si los parámetros son válidos
            if not table_locator or row <= 0 or column <= 0:
                return self.default_response(action="extract_table_data", element=table_locator, status="fail", error="Los parámetros table_locator, row o column no son válidos.")
            
            # Esperar hasta que la tabla esté presente
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(table_locator))

            # Encontrar la tabla
            table = driver.find_element(*table_locator)

            # Usar xpath para seleccionar la celda específica
            cell = table.find_element_by_xpath(f".//tr[{row}]/td[{column}]")

            # Extraer el texto de la celda
            cell_data = cell.text

            # Retornar la respuesta con éxito
            return self.default_response(action="extract_table_data", element=table_locator, status="success", row=row, column=column, cell_data=cell_data)
        
        except TimeoutException:
            # Manejar el caso en que la tabla no se encuentra en el tiempo esperado
            return self.default_response(action="extract_table_data", element=table_locator, status="fail", error="TimeoutException: No se encontró la tabla en el tiempo esperado.")
        
        except NoSuchElementException:
            # Manejar el caso en que la tabla o celda no se encuentran
            return self.default_response(action="extract_table_data", element=table_locator, status="fail", error=f"NoSuchElementException: No se encontró la tabla o la celda en la fila {row} y columna {column}.")
        
        except Exception as e:
            # Capturar cualquier otro error inesperado
            return self.default_response(action="extract_table_data", element=table_locator, status="fail", error=f"Error inesperado: {str(e)}")
