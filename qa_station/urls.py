"""
URL configuration for qa_station project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('about_us/', include('about_us.urls')),
    path('documentation/', include('user_documentation.urls')),
    path('projects/', include('user_projects.urls', namespace='user_projects')),
    path('tests/', include('functional_tests.urls', namespace='functional_tests')),
    path('ai_module/', include('ai_module.urls', namespace='ai_module'))

]
