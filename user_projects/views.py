from django.shortcuts import render

# Renderizar la página principal
def project_view(request):
    print("Vista user_project llamada")
    return render(request, 'user_projects/user_project.html')