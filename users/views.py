from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm

# Renderizar la página principal
def main_view(request):
    print("Vista main_page llamada")
    return render(request, 'users/login.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Autenticación directa
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido/a {user.username}')
                return redirect('about_us')
            else:
                form.add_error('password', "La contraseña ingresada es incorrecta.")
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = CustomAuthenticationForm()

    if 'next' in request.GET or request.GET.get('logged_out') == '1':
        messages.info(request, 'Has cerrado sesión exitosamente.')

    return render(request, 'users/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect(f"{reverse('users:login')}?logged_out=1")

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada con éxito.')
            return redirect('users:login')
        else:
            messages.error(request, 'Ocurrió un error en el registro. Por favor, revisa los datos ingresados.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

# Vista para restablecer la contraseña (solicitud)
def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            # Aquí puedes generar el código o link de verificación para enviar por correo
            # Puedes usar la función send_mail o cualquier otra forma de enviar correos.
            send_mail(
                'Recupera tu contraseña',
                'Aquí está tu código de recuperación...',  # Mensaje del correo
                'noreply@qastation.com',  # Email remitente
                [user.email],  # Destinatarios
            )
            messages.success(request, 'Revisa tu correo para continuar con el proceso.')
            return redirect('password_reset_confirm')
        except User.DoesNotExist:
            messages.error(request, 'No se encontró una cuenta con ese correo electrónico.')
    return render(request, 'users/password_reset.html')

# Vista para ingresar el código de verificación
def password_reset_confirm_view(request):
    if request.method == 'POST':
        # Aquí puedes manejar el código de verificación y restablecimiento
        token = request.POST['token']
        new_password = request.POST['new_password']
        # Verificar si el token es válido y luego restablecer la contraseña
        user = User.objects.get(email=request.POST['email'])
        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Contraseña restablecida con éxito.')
            return redirect('login')
        else:
            messages.error(request, 'El código de verificación es incorrecto.')
    return render(request, 'users/password_reset_confirm.html')