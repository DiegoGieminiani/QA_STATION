from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TestRunSerializer  # Importa el serializer para validar el JSON
from functional_tests.runner import TestRunner  # Importa el TestRunner para ejecutar las pruebas

class ExecuteTestsAPI(APIView):
    def post(self, request):
        # Obtener los datos JSON de la solicitud
        json_data = request.data

        # Validar el JSON usando el serializer
        serializer = TestRunSerializer(data=json_data)
        
        # Si el JSON es válido, ejecutar las pruebas
        if serializer.is_valid():
            try:
                # Pasar los datos validados al TestRunner
                runner = TestRunner(serializer.validated_data)
                result = runner.run_tests()

                # Retornar los resultados de las pruebas
                return Response(result, status=status.HTTP_200_OK)
            
            except Exception as e:
                # Si ocurre un error en la ejecución de las pruebas, devolver un mensaje de error
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Si el JSON no es válido, devolver los errores de validación
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
