from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from functional_tests.models import FunctionalTest  # Cambia la ruta de importación aquí
from .serializers import TestRunSerializer
from functional_tests.process_automatic_test_cases import process_automatic_test_cases


class ExecuteTestsAPI(APIView):
    """
    Endpoint para recibir y procesar casos de prueba.
    """

    def post(self, request):
        # Recibir JSON
        json_data = request.data

        # Validar JSON con el serializer
        serializer = TestRunSerializer(data=json_data, many=True)

        if serializer.is_valid():
            try:
                # Procesar pruebas automáticas
                processed_tests = process_automatic_test_cases(serializer.validated_data)

                # Verificar resultados individuales
                if not processed_tests['individual_results']:
                    return Response({'error': 'No results found'}, status=status.HTTP_204_NO_CONTENT)

                return Response(processed_tests, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': f'Exception: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Si el serializer falla
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
