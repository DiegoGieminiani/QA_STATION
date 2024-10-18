import os
import time

def take_screenshot(driver, action_name, delay=0):
    # Añadir un retraso antes de tomar el screenshot
    if delay > 0:
        time.sleep(delay)

    # Ruta a la carpeta 'media' dentro de 'screenshots'
    screenshot_dir = os.path.join('functional_tests', 'selenium_test', 'screenshots', 'media')
    
    # Si la carpeta no existe, crearla
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    # Crear el nombre del archivo con un timestamp
    timestamp = int(time.time())
    screenshot_path = os.path.join(screenshot_dir, f"{action_name}_{timestamp}.png")
    
    # Tomar la captura de pantalla
    driver.save_screenshot(screenshot_path)
    
    return screenshot_path
