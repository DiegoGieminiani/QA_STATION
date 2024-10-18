from functional_tests.selenium_test.base_action import BaseAction
from selenium.common.exceptions import JavascriptException

class ExecuteScriptAction(BaseAction):
    def execute(self, script, *args, **kwargs):
        try:
            # Validar que el script no sea nulo o vacío
            if not script:
                return self.default_response(
                    action="execute_script",
                    element="script",
                    status="fail",
                    error="El script proporcionado está vacío o es inválido."
                )

            # Ejecutar el script de JavaScript en el contexto de la página actual
            result = self.driver.execute_script(script, *args)

            # Retornar el resultado del script ejecutado
            return self.default_response(
                action="execute_script",
                element="script",
                status="success",
                result=result,
                script_executed=script,
                args=args
            )

        except JavascriptException as e:
            # Capturar cualquier excepción de JavaScript y retornar el error
            return self.default_response(
                action="execute_script",
                element="script",
                status="fail",
                error=f"Error en la ejecución del script: {str(e)}"
            )

        except Exception as e:
            # Capturar cualquier otra excepción y retornar el error
            return self.default_response(
                action="execute_script",
                element="script",
                status="fail",
                error=f"Error inesperado: {str(e)}"
            )
