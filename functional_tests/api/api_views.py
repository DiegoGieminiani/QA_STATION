from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TestRunSerializer
from .test_case_processor import process_test_cases

class ExecuteTestsAPI(APIView):
    def post(self, request):
        json_data = request.data

        # Validar el JSON
        serializer = TestRunSerializer(data=json_data, many=True)

        if serializer.is_valid():
            try:
                # Procesar las pruebas (ya ejecuta el TestRunner dentro de process_test_cases)
                processed_tests = process_test_cases(serializer.validated_data)

                # Verifica que los resultados no estén vacíos
                if not processed_tests['individual_results']:
                    print("Error: Lista de resultados vacía.")
                    return Response({'error': 'No results found'}, status=status.HTTP_204_NO_CONTENT)

                # Imprimir la lista de resultados completa
                print(f"Lista final de resultados: {processed_tests['individual_results']}")

                # Devuelve los resultados correctamente
                return Response(processed_tests, status=status.HTTP_200_OK)

            except NameError as e:
                print(f"Error en la ejecución (NameError): {str(e)}")
                return Response({'error': f'NameError: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                print(f"Error en la ejecución: {str(e)}")
                return Response({'error': f'Exception: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Si la validación del serializer falla
        print(f"Errores de validación: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
