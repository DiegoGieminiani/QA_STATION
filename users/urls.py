from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import main_view, register_view, login_view, password_reset_view

app_name = 'users'

urlpatterns = [
    path('', main_view, name='main_page'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('password_reset/', password_reset_view, name='password_reset'),
    # Usar la vista de Django para logout
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout')
    
]
