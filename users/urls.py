from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset_confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),
]
