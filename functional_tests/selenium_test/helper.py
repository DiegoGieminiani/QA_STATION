import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def initialize_chrome_driver():
    """Inicializa el navegador Chrome con opciones predeterminadas."""
    # Instalar ChromeDriver automáticamente si no está presente
    chromedriver_autoinstaller.install()
    
    # Opciones del navegador Chrome
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Ejecutar en segundo plano (sin interfaz visible)
    chrome_options.add_argument("--incognito")  # Ejecutar en modo incógnito
    chrome_options.add_argument("--disable-gpu")  # Deshabilitar GPU para mejorar rendimiento

    # Inicializamos el driver de Chrome con las opciones configuradas
    driver = webdriver.Chrome(options=chrome_options)
    
    # Borrar todas las cookies antes de comenzar
    driver.delete_all_cookies()
    print("Cookies eliminadas con éxito.")
    
    return driver
