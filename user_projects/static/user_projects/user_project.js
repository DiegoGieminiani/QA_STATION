// Cuando se haga clic en un proyecto
document.querySelectorAll(".project-card").forEach((card) => {
  card.addEventListener("click", function (event) {
    event.preventDefault();
    const projectId = this.getAttribute("id");
    showProjectDetails(projectId);
  });
});

// Muestra los detalles del proyecto con nombre y descripción
function showProjectDetails(projectId) {
  const projectDetails = document.getElementById("projectDetails");
  let projectName = "";
  let projectDescription = "";

  switch (projectId) {
    case "project1":
      projectName = "Google Testing";
      projectDescription =
        "Este proyecto implica pruebas para el motor de búsqueda de Google.";
      break;
    case "project2":
      projectName = "Duoc Page Testing";
      projectDescription = "Pruebas para el sitio web institucional de Duoc.";
      break;
    case "project3":
      projectName = "QA Station Testing";
      projectDescription =
        "Proyecto para automatizar y gestionar pruebas de calidad en QA Station.";
      break;
    default:
      projectName = "Proyecto no encontrado";
      projectDescription = "Descripción no disponible.";
  }

  projectDetails.innerHTML = `<h2>${projectName}</h2><p>${projectDescription}</p>`;
  document.getElementById("addProjectForm").style.display = "none"; // Oculta el formulario si está visible
}

// Muestra el formulario para agregar un nuevo proyecto
document
  .querySelector(".project-card-add")
  .addEventListener("click", function (event) {
    event.preventDefault();
    document.getElementById("addProjectForm").style.display = "block";
    document.getElementById("projectDetails").innerHTML = ""; // Oculta cualquier detalle de proyecto cuando el formulario está visible
  });

// Agregar un nuevo proyecto
document
  .getElementById("newProjectForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const newProjectName = document.getElementById("projectName").value;
    const newProjectDescription =
      document.getElementById("projectDescription").value; // Obtiene la descripción del formulario
    const projectGrid = document.querySelector(".projects-grid");

    // Crear una nueva tarjeta de proyecto
    const newProjectCard = document.createElement("div");
    newProjectCard.setAttribute("id", newProjectName);
    newProjectCard.classList.add("project-card");
    newProjectCard.innerHTML = `<span class="project-title">${newProjectName}</span><p class="project-description">${newProjectDescription}</p>`;

    // Asignar funcionalidad a la nueva tarjeta de proyecto
    newProjectCard.addEventListener("click", function (event) {
      event.preventDefault();
      showProjectDetails(newProjectName, newProjectDescription); // Pasa el nombre y descripción
    });

    // Agregar la nueva tarjeta al grid
    projectGrid.appendChild(newProjectCard);

    // Mostrar el nuevo proyecto en los detalles
    document.getElementById(
      "projectDetails"
    ).innerHTML = `<h2>${newProjectName}</h2><p>${newProjectDescription}</p>`;

    // Ocultar el formulario después de agregar el proyecto
    document.getElementById("addProjectForm").style.display = "none";
  });
