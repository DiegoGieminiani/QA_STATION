from functional_tests.selenium_test.base_action import BaseAction

class ImplicitWaitAction(BaseAction):
    def execute(self, timeout=10, **kwargs):
        try:
            # Establecer la espera implícita para el driver
            self.driver.implicitly_wait(timeout)

            # Retornar respuesta estándar con éxito
            return self.default_response(action="implicit_wait", status="success", timeout=timeout)

        except Exception as e:
            # Capturar cualquier error que ocurra al configurar la espera implícita
            return self.default_response(action="implicit_wait", status="fail", error=str(e))
