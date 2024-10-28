from rest_framework import serializers

class ActionSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=50)
    element_type = serializers.CharField(max_length=50, required=False)  # Opcional para algunas acciones
    value = serializers.CharField(max_length=255, required=False)  # Opcional para algunas acciones
    input_value = serializers.CharField(max_length=255, required=False)  # Opcional para algunas acciones
    expected_value = serializers.CharField(max_length=255, required=False)  # Para verificar URL o valores esperados

    def validate(self, data):
        action = data.get('action')

        # Validar que 'element_type' y 'value' sean obligatorios para acciones específicas
        actions_requiring_element_and_value = ["click", "enter_data", "select", "verify_text"]
        if action in actions_requiring_element_and_value:
            if not data.get('element_type') or not data.get('value'):
                raise serializers.ValidationError("Los campos 'element_type' y 'value' son obligatorios para esta acción.")

        # Validar que 'input_value' sea obligatorio para 'enter_data' y 'select'
        if action in ["enter_data", "select"] and not data.get('input_value'):
            raise serializers.ValidationError("El campo 'input_value' es obligatorio para la acción 'enter_data' o 'select'.")

        # Validar que 'expected_value' sea obligatorio para 'verify_text'
        if action == "verify_text" and not data.get('expected_value'):
            raise serializers.ValidationError("El campo 'expected_value' es obligatorio para 'verify_text'.")

        return data