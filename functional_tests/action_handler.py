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

NO_ELEMENT_ACTIONS = [
    "accept_alert", "alert_is_present", "confirm_alert", "dismiss_alert", 
    "enter_prompt", "prompt_alert", "execute_script", "back", "forward", 
     "refresh", "switch_tab", "verify_url","navigate_to_url"
]

ELEMENT_ACTIONS = [
    "click", "enter_data", "verify_text", "select", "extract_attribute", 
    "extract_dropdown_options", "extract_links", "extract_list_items", 
    "extract_table_data", "extract_text", "check_checkbox", "clear_field", 
    "select_radio_button", "submit_form", "change_element_style", 
    "get_element_property", "scroll_into_element", "send_keys", "drag_and_drop", 
    "context_click", "double_click", "click_and_hold", "hover", "release", 
    "scroll", "close_modal", "enter_data_in_modal", "open_modal", 
    "submit_modal_form", "verify_modal_vision", "scroll_to_element", 
    "verify_attribute_value", "verify_element_has_child", 
    "verify_element_presence", "verify_element_selected"
]
def execute_action(action_instance, action, element_type=None, selector_value=None, **kwargs):
    """
    Ejecutar la acción usando la instancia mapeada.

    Args:
        action_instance: Instancia de la acción a ejecutar.
        action: Nombre de la acción.
        element_type: Tipo de elemento (si aplica).
        selector_value: Valor del selector (si aplica).
        **kwargs: Parámetros adicionales para la acción.

    Returns:
        Resultado de la ejecución de la acción.
    """
    try:
        # Acciones que no requieren elementos
        if action in NO_ELEMENT_ACTIONS:
            result = action_instance.execute(**kwargs)
        
        # Acciones que requieren elementos (element_type y selector_value)
        elif action in ELEMENT_ACTIONS:
            if element_type and selector_value:
                result = action_instance.execute(element_type, selector_value, **kwargs)
            else:
                raise ValueError(f"Faltan parámetros para la acción: {action}")
        else:
            raise ValueError(f"Acción desconocida: {action}")

        if not result:
            return {'action': action, 'status': 'fail', 'message': 'Resultado vacío'}

        return result

    except Exception as e:
        return {'action': action, 'status': 'fail', 'message': str(e)}
    
    
def retry_action(action_function, retries, log_message, *args, **kwargs):
    """Manejar los reintentos de una acción en caso de fallos."""
    for attempt in range(retries):
        log_message(f"Intentando acción {args[0]} (Intento {attempt + 1})")
        result = action_function(*args, **kwargs)
        if result.get('status') == 'success':
            return result
        log_message(f"Reintentando acción {args[0]} en 4 segundos (Intento {attempt + 1})")
        time.sleep(4)
    log_message(f"Acción {args[0]} fallida después de {retries} intentos")
    return result
