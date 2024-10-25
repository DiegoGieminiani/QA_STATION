// Cuando se haga clic en un proyecto
document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('click', function(event) {
        event.preventDefault();
        const projectId = this.getAttribute('id');
        showProjectDetails(projectId);
    });
});

// Muestra los detalles del proyecto
function showProjectDetails(projectId) {
    const projectDetails = document.getElementById('projectDetails');
    let projectName = '';
    
    switch (projectId) {
        case 'project1':
            projectName = 'Google Testing';
            break;
        case 'project2':
            projectName = 'Duoc Page Testing';
            break;
        case 'project3':
            projectName = 'QA Station Testing';
            break;
        default:
            projectName = 'Proyecto no encontrado';
    }

    projectDetails.innerHTML = `<h2>${projectName}</h2><p>Detalles del proyecto ${projectName}...</p>`;
    document.getElementById('addProjectForm').style.display = 'none'; // Oculta el formulario si está visible
}

// Muestra el formulario para agregar un nuevo proyecto
document.querySelector('.project-card-add').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('addProjectForm').style.display = 'block';
    document.getElementById('projectDetails').innerHTML = ''; // Oculta cualquier detalle de proyecto cuando el formulario está visible
});

// Agregar un nuevo proyecto
document.getElementById('newProjectForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const newProjectName = document.getElementById('projectName').value;
    const projectGrid = document.querySelector('.projects-grid');
    
    // Crear una nueva tarjeta de proyecto
    const newProjectCard = document.createElement('div');
    newProjectCard.setAttribute('id', newProjectName);
    newProjectCard.classList.add('project-card');
    newProjectCard.innerHTML = `<span class="project-title">${newProjectName}</span>`;

    // Asignar funcionalidad a la nueva tarjeta de proyecto
    newProjectCard.addEventListener('click', function(event) {
        event.preventDefault();
        showProjectDetails(newProjectName);
    });

    // Agregar la nueva tarjeta al grid
    projectGrid.appendChild(newProjectCard);

    // Mostrar el nuevo proyecto en los detalles
    document.getElementById('projectDetails').innerHTML = `<h2>${newProjectName}</h2><p>Detalles del proyecto ${newProjectName}...</p>`;
    
    // Ocultar el formulario después de agregar el proyecto
    document.getElementById('addProjectForm').style.display = 'none';
});
