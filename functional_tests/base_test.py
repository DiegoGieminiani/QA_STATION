from selenium.webdriver.chrome.webdriver import WebDriver
from .helper import initialize_chrome_driver  # Importar la función compartida
from django.test import TestCase  # Asegurarse de que TestCase de Django esté importado

class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración antes de iniciar las pruebas."""
        # Inicializamos el driver de Chrome usando la función compartida
        cls.driver: WebDriver = initialize_chrome_driver()

    @classmethod
    def tearDownClass(cls):
        """Cierra el navegador al finalizar las pruebas."""
        cls.driver.quit()
