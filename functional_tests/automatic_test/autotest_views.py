from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TestRunSerializer

class ExecuteTestsAPI(APIView):
    
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
            user = None  # Aquí puedes asignar el usuario real en tu lógica
            print("Usuario asignado:", user)

            # Crear instancia del manejador de ejecución de pruebas con el usuario asignado
            handler = TestExecutionHandler(serializer.validated_data, user=user)
            print("Datos validados del serializer:", serializer.validated_data)

            # Guardar los casos de prueba sin ejecutar aún
            save_status = handler.save_tests()
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
