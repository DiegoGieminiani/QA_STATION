from django.urls import path
from .views import main_view, register_view, login_view, password_reset_view

urlpatterns = [
    path('', main_view, name='main_page'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('password_reset/', password_reset_view, name='password_reset')
  #  path('password_reset_confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),
]
