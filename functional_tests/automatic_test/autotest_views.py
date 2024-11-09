from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TestRunSerializer
from django.contrib.auth.models import User
from functional_tests.models import FunctionalTest

class ExecuteTestsAPI(APIView):
    
    def save_tests(self, validated_data):
        #Desglosa y guarda los casos de prueba en FunctionalTest sin ejecutarlos.
        try:
            print("*\n"*50)
            print(validated_data)
            print("*\n"*50)

            print(validated_data[0]["actions"])
            for test in validated_data[0]["actions"]:
                if not all(key in test for key in ['url', 'actions']):
                    raise ValidationError("Cada caso de prueba debe incluir 'url' y 'actions'.")
                nuevo_functional_test = TestCase(
                    actions_data=validated_data.action,
                    name=mensaje_usuario,
                    project_id=15
                )
                
            # Llamada a process_automatic para desglosar y guardar los casos
            save_status = automatic_process(self.validated_data, self.project, self.test_case)
            return save_status # Devuelve el estado del guardado
        except Exception as e:
            return {'error': f'Error al guardar casos de prueba: {str(e)}', 'status': 'error'}

    def post(self, request):
        from .test_execution_handler import TestExecutionHandler
        json_data = request.data

        # Imprimir el JSON recibido para verificar la entrada
        print("JSON recibido:", json_data)

        # Validar el JSON
        serializer = TestRunSerializer(data=json_data, many=True)
        print("Estado de validación del serializer:", serializer.is_valid())

        if serializer.is_valid():
            # Intentar obtener el usuario con ID 2, y si no existe, crearlo
            # Asumiendo que tienes algún código para crear o asignar el usuario
            user = User.objects.get(id=2)  # Aquí puedes asignar el usuario real en tu lógica
            print("Usuario asignado:", user)

            # Guardar los casos de prueba sin ejecutar aún
            save_status = self.save_tests(serializer.validated_data)
            print("Estado de guardado de los casos de prueba:", save_status)

            # Verificar si el guardado fue exitoso
            if 'error' in save_status:
                print("Error al guardar los casos de prueba:", save_status['error'])
                return Response({'error': save_status['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Retornar una respuesta de éxito indicando que los casos se guardaron correctamente
            return Response({'message': 'Casos de prueba guardados exitosamente', 'test_case_id': save_status['test_case_id']}, status=status.HTTP_200_OK)

        # Si la validación del serializer falla
        print("Errores de validación del serializer:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
