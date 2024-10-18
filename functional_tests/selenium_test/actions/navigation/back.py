from functional_tests.selenium_test.base_action import BaseAction

class BackAction(BaseAction):
    def execute(self, **kwargs):
        try:
            # Ir hacia atrás en el navegador
            self.driver.back()

            # Retornar la respuesta estándar de éxito
            return self.default_response(action='go_back', element='Navegador', status='success')

        except Exception as e:
            # Capturar cualquier error inesperado
            return self.default_response(action='go_back', element='Navegador', status='fail', error=str(e))
