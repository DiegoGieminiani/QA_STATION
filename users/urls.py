from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import main_view, register_view, login_view, password_reset_view
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('', main_view, name='main_page'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    
    #path('password_reset/', password_reset_view, name='password_reset'),
    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
