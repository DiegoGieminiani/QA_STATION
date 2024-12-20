from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def project_view(request):
    projects = Project.objects.filter(user=request.user)  # Filtrar solo proyectos del usuario actual
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)  # Corregido aquí
            project.user = request.user  # Asigna el proyecto al usuario autenticado
            project.save()
            return redirect('projects')
    else:
        form = ProjectForm()

    return render(request, 'user_projects/user_project.html', {
        'projects': projects,
        'form': form
    })

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Detecta si es una solicitud AJAX
        return JsonResponse({
            'name': project.name,
            'description': project.description
        })
    else:
        test_cases = project.test_cases.all()  # Obtiene los TestCases relacionados
        return render(request, 'user_projects/project_detail.html', {'project': project, 'test_cases': test_cases})

@login_required 
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

@login_required 
def select_project(request):
    projects = Project.objects.filter(user=request.user)  # Obtiene los proyectos del usuario actual
    return render(request, 'user_projects/user_select.html', {'projects': projects})
