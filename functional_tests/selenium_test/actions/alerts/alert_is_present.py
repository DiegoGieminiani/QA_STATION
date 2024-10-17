from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functional_test.selenium_test.base_action import BaseAction

class AlertIsPresentAction(BaseAction):
    def __init__(self, driver):
        super().__init__(driver)
    
    def execute(self, driver, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())

