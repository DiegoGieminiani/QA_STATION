from rest_framework import serializers
from functional_test.runner import TestRunner


class ActionSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=50)
    element_type = serializers.CharField(max_length=50, required=False)  # Opcional
    value = serializers.CharField(max_length=255, required=False)  # Opcional
    input_value = serializers.CharField(max_length=255, required=False)  # Opcional
    expected_value = serializers.CharField(max_length=255, required=False)  # Para verificar URL

    def validate(self, data):
        action = data.get('action')

        # Validar que 'element_type' y 'value' sean obligatorios para acciones específicas
        actions_requiring_element_and_value = ["click", "enter_data", "select", "verify_text"]
        if action in actions_requiring_element_and_value:
            if not data.get('element_type') or not data.get('value'):
                raise serializers.ValidationError("The fields 'element_type' and 'value' are required for this action.")

        # Validar que 'expected_value' sea obligatorio para 'verify_url'
        if action == "verify_url" and not data.get('expected_value'):
            raise serializers.ValidationError("The field 'expected_value' is required for the 'verify_url' action.")
        
        # Debug: Verificar que 'expected_value' llega correctamente
        if action == "verify_url":
            print(f"Validando verify_url con expected_value: {data.get('expected_value')}")

        # Validar que 'input_value' sea obligatorio para 'enter_data' y 'select'
        if action in ["enter_data", "select"] and not data.get('input_value'):
            raise serializers.ValidationError("The 'input_value' field is required for 'enter_data' or 'select'.")

        # Validar que 'input_value' no esté presente para la acción 'click'
        if action == 'click' and data.get('input_value'):
            raise serializers.ValidationError("The 'input_value' field should not be present for the 'click' action.")
        
        return data


class TestRunSerializer(serializers.Serializer):
    url = serializers.URLField()  # La URL de la página que se va a probar
    actions = ActionSerializer(many=True)  # Una lista de acciones a ejecutar

    def validate(self, data):
        # Validar que haya al menos una acción
        if not data.get('actions'):
            raise serializers.ValidationError("At least one action must be provided.")

        # Validar que la URL esté presente
        if not data.get('url'):
            raise serializers.ValidationError("The URL field is required.")

        return data

    def create(self, validated_data):
        
        # Aquí ejecutamos la lógica de pruebas basadas en los datos validados
        url = validated_data['url']
        actions_data = validated_data['actions']
        

        # Llamar al TestRunner para ejecutar las pruebas
        runner = TestRunner(url, actions_data)
        result = runner.run_tests()  # Ejecutar las pruebas y retornar resultados

        return result
