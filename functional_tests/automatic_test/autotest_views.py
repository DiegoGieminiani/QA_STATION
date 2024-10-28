from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TestRunSerializer


class ExecuteTestsAPI(APIView):
    
    def post(self, request):
        from .test_execution_handler import TestExecutionHandler
        json_data = request.data

        # Validar el JSON
        serializer = TestRunSerializer(data=json_data, many=True)

        if serializer.is_valid():
            # Crear instancia del manejador de ejecución de pruebas
            handler = TestExecutionHandler(serializer.validated_data)

            # Guardar los casos de prueba sin ejecutar aún
            save_status = handler.save_tests()

            # Verificar si el guardado fue exitoso
            if 'error' in save_status:
                return Response({'error': save_status['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Retornar una respuesta de éxito indicando que los casos se guardaron correctamente
            return Response({'message': 'Casos de prueba guardados exitosamente', 'test_case_id': save_status['test_case_id']}, status=status.HTTP_200_OK)

        # Si la validación del serializer falla
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
