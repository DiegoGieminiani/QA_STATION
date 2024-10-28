from rest_framework import serializers
from .action_serializers import ActionSerializer


class TestRunSerializer(serializers.Serializer):
    url = serializers.URLField()  # La URL de la página que se va a probar
    actions = ActionSerializer(many=True)  # Lista de acciones a ejecutar

    def validate(self, data):
        # Validar que haya al menos una acción
        if not data.get('actions'):
            raise serializers.ValidationError("Se debe proporcionar al menos una acción.")

        # Validar que la URL esté presente
        if not data.get('url'):
            raise serializers.ValidationError("El campo URL es obligatorio.")

        return data

    def create(self, validated_data):
        # Este método es para crear la representación validada de los datos
        return validated_data
