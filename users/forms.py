from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico", required=True)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        
        if email and password:
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if user is None:
                    self.add_error("password", "Contraseña incorrecta. Intente de nuevo.")
            except User.DoesNotExist:
                self.add_error("email", "El correo no existe. Verifique e intente nuevamente.")
        return cleaned_data