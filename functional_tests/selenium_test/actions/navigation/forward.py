from functional_test.selenium_test.base_action import BaseAction

class ForwardAction(BaseAction):
    def execute(self, **kwargs):
        try:
            # Ir hacia adelante en el navegador
            self.driver.forward()

            # Retornar la respuesta estándar de éxito
            return self.default_response(action='go_forward', element='Navegador', status='success')

        except Exception as e:
            # Capturar cualquier error inesperado
            return self.default_response(action='go_forward', element='Navegador', status='fail', error=str(e))
