import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def resolve_variables(stored_values, kwargs):
    """Resolver variables dinámicas en los argumentos de la acción."""
    for key, value in kwargs.items():
        if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
            variable_name = value[2:-1]
            kwargs[key] = stored_values.get(variable_name, value)
    return kwargs

def handle_alert(driver, action, log_message):
    """Manejar alertas para acciones como accept_alert o enter_prompt."""
    if action in ["accept_alert", "enter_prompt"]:
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
        except TimeoutException:
            log_message(f"No se encontró ninguna alerta presente para la acción {action}")
            return {'action': action, 'element': 'alert', 'status': 'fail'}
    return None

NO_ELEMENT_ACTIONS = ["accept_alert", "switch_tab", "verify_url"]
ELEMENT_ACTIONS = ["click", "enter_data", "verify_text"]

def execute_action(action_instance, action, element_type=None, selector_value=None, **kwargs):
    """Ejecutar la acción usando la instancia mapeada."""
    try:
        if action in NO_ELEMENT_ACTIONS:
            return action_instance.execute(**kwargs)

        elif action in ELEMENT_ACTIONS:
            if element_type and selector_value:
                return action_instance.execute(element_type, selector_value, **kwargs)
            else:
                raise ValueError(f"Faltan parámetros para la acción: {action}")

        else:
            raise ValueError(f"Acción desconocida: {action}")

    except TimeoutException:
        raise TimeoutWaitingForElementException(element_type, selector_value)

    except NoSuchElementException:
        raise ElementNotFoundException(element_type, selector_value)

    except Exception as e:
        return {'action': action, 'status': 'fail', 'error': str(e)}
    
    
def retry_action(action_function, retries, log_message, *args, **kwargs):
    """Manejar los reintentos de una acción en caso de fallos."""
    for attempt in range(retries):
        result = action_function(*args, **kwargs)
        if result.get('status') == 'success':
            return result
        log_message(f"Reintentando acción {args[0]} en 4 segundos (Intento {attempt + 1})")
        time.sleep(4)
    return result
