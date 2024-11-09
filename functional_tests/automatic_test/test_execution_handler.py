from .automatic_process import automatic_process
from functional_tests.models import FunctionalTest, Result
from functional_tests.runner import TestRunner
from user_projects.models import Project
from ai_module.models import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TestExecutionHandler:
    def __init__(self, validated_data, user=None, project=None, test_case=None):
        """        # Intenta obtener o asignar el usuario con user_id = 2 y verifica que es una instancia de User
        try:
            self.user = user or User.objects.get(id=2)
        except User.DoesNotExist:
            # Si el usuario no existe, crearlo como un usuario de prueba
            self.user = User.objects.create_user(
                id=2,
                username="johndoe",
                email="john.doe@example.com",
                password="ContraseñaSegura123"
            )
        # Verifica que `self.user` sea una instancia de User antes de continuar
        if not isinstance(self.user, User):
            raise ValueError("El usuario proporcionado no es una instancia válida de User.")
        """
        # Crear instancias de prueba si project o test_case no están definidos
        self.project = project or Project.objects.create(name="Proyecto de prueba")
        self.test_case = test_case or TestCase.objects.create(name="Caso de prueba")
        self.validated_data = validated_data

    def save_tests(self, validated_data):
        print("SAPO")
        print(self)
        print("SAPO 2")
        print(validated_data)
        #Desglosa y guarda los casos de prueba en FunctionalTest sin ejecutarlos.

        try:
            print(self.validated_data)  # Imprimir los datos validados para verificar la entrada
             # Validación adicional: confirmar que self.validated_data tiene la estructura esperada
            if not isinstance(self.validated_data, list):
                raise ValidationError("validated_data debe ser una lista de casos de prueba.")

            for test in self.validated_data:
                if not all(key in test for key in ['url', 'actions']):
                    raise ValidationError("Cada caso de prueba debe incluir 'url' y 'actions'.")

            # Llamada a process_automatic para desglosar y guardar los casos
            save_status = automatic_process(self.validated_data, self.project, self.test_case)
            return save_status # Devuelve el estado del guardado
            
        except ValidationError as ve:
            return {'error': f'Error de validación: {str(ve)}', 'status': 'error'}
        except Exception as e:
            return {'error': f'Error al guardar casos de prueba: {str(e)}', 'status': 'error'}

    def run_saved_tests(self):
        #Recupera y ejecuta los casos de prueba guardados en FunctionalTest, y guarda los resultados en Result.
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

            # Guardar el resultado en Result, asociándolo con el usuario
            result_record = Result.objects.create(
                status=result['result'],
                description='Descripción del resultado de la prueba',
                evidence=None,  # Puedes ajustar esto según los datos de evidencia que tengas
                test_results=result['actions'],
                functional_test=functional_test,
                user=self.user  # Asegurar que user es una instancia válida de User
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
