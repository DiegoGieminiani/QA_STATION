from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico", required=True)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            # Verificar si el correo existe en la base de datos
            try:
                user = User.objects.get(email=email)
                # Autenticar usando el username del usuario
                user = authenticate(username=user.username, password=password)
                if user is None:
                    self.add_error("password", "La contraseña ingresada es incorrecta. Por favor, intenta nuevamente o restablece tu contraseña si la has olvidado.")
            except User.DoesNotExist:
                self.add_error("email", "El correo electrónico ingresado no existe. Por favor, verifica e intenta nuevamente.")

        return cleaned_data
