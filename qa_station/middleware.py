from django.shortcuts import redirect
import re

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define las rutas que requieren autenticación
        self.login_required_paths = [
            re.compile(r'^//'),
            re.compile(r'^//'),
            re.compile(r'^//')  
        ]

    def __call__(self, request):
        print(f"Middleware ejecutado para la ruta: {request.path}")  # Añade esta línea para depuración
        # Verifica si el usuario no está autenticado y la ruta requiere autenticación
        if not request.user.is_authenticated:
            for path in self.login_required_paths:
                if path.match(request.path):
                    print("Redirigiendo a login")  # Mensaje de depuración
                    return redirect('/users/login')  
        return self.get_response(request)
