from .process_automatic import process_automatic
from functional_tests.models import FunctionalTest, Result
from functional_tests.runner import TestRunner

class TestExecutionHandler:
    def __init__(self, validated_data, project, test_case):
        self.validated_data = validated_data
        self.project = project
        self.test_case = test_case

    def save_tests(self):
        """
        Desglosa y guarda los casos de prueba en FunctionalTest sin ejecutarlos.
        """
        try:
            # Llamada a process_automatic para desglosar y guardar los casos
            save_status = process_automatic(self.validated_data, self.project, self.test_case)
            return save_status
        except Exception as e:
            return {'error': f'Error al guardar casos de prueba: {str(e)}', 'status': 'error'}

    def run_saved_tests(self):
        """
        Recupera y ejecuta los casos de prueba guardados en FunctionalTest, y guarda los resultados en Result.
        """
        results = []
        global_results = []

        # Recuperar todos los casos guardados para el test_case actual
        functional_tests = FunctionalTest.objects.filter(test_case=self.test_case)

        if not functional_tests.exists():
            return {'error': 'No hay casos de prueba guardados para ejecutar', 'status': 'empty'}

        # Ejecutar cada caso de prueba guardado
        for functional_test in functional_tests:
            print(f"Ejecutando Prueba {functional_test} con datos: {functional_test.json_data}")
            runner = TestRunner(functional_test.json_data)
            result = runner.run_tests()

            # Guardar el resultado en Result
            result_record = Result.objects.create(
                status=result['result'],
                description='Descripción del resultado de la prueba',
                evidence=None,  # Puedes ajustar esto según los datos de evidencia que tengas
                test_results=result['actions'],
                functional_test=functional_test
            )

            # Guardar resultados individuales y globales
            results.append({
                'id': functional_test.id,
                'result': result['result'],
                'actions': result['actions']
            })

            global_results.append({
                'id': functional_test.id,
                'result': result['result']
            })

        return {
            'individual_results': results,
            'global_results': global_results
        }
