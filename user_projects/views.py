from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

# Vista para listar proyectos
def project_view(request):
    # Mostrar todos los proyectos en la página principal
    projects = Project.objects.all()
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user  # Asociar el proyecto al usuario actual
            project.save()
            return redirect('projects')  # Recargar la página para ver el nuevo proyecto en la lista
    else:
        form = ProjectForm()

    return render(request, 'user_projects/user_project.html', {
        'projects': projects,
        'form': form
    })

# Vista para ver el detalle de un proyecto
def project_detail(request, project_id):
   project = get_object_or_404(Project, id=project_id)
   test_cases = project.test_cases.all()  # Obtiene los TestCases relacionados
   return render(request, 'user_projects/project_detail.html', {'project': project, 'test_cases': test_cases})

# Vista para agregar un proyecto
@login_required  # Asegura que solo usuarios autenticados puedan acceder
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)  # No guardes aún en la base de datos
            project.user = request.user  # Asigna el usuario actual
            project.save()  # Ahora guarda el proyecto con el usuario asignado
            return redirect('projects')  # Redirige a la lista de proyectos
    else:
        form = ProjectForm()
    return render(request, 'user_projects/user_project.html', {'form': form})