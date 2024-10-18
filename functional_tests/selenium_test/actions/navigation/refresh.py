from functional_tests.selenium_test.base_action import BaseAction

class RefreshPageAction(BaseAction):
    def execute(self, **kwargs):
        try:
            # Refrescar la página
            self.driver.refresh()

            # Retornar la respuesta estándar de éxito
            return self.default_response(action='refresh_page', element='Navegador', status='success')

        except Exception as e:
            # Capturar cualquier error inesperado
            return self.default_response(action='refresh_page', element='Navegador', status='fail', error=str(e))
