// Cuando se haga clic en un proyecto
document.querySelectorAll(".project-card").forEach((card) => {
  card.addEventListener("click", function (event) {
    event.preventDefault();
    const projectId = this.getAttribute("data-id"); // Usa el atributo data-id para obtener el ID del proyecto
    fetchProjectDetails(projectId); // Llama a la función para obtener los detalles desde el servidor
  });
});

// Función para hacer una solicitud AJAX para obtener los detalles del proyecto
function fetchProjectDetails(projectId) {
  fetch(`/projects/${projectId}/`) // Asume que la URL de detalle es /projects/<project_id>/
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error al obtener los detalles del proyecto");
      }
      return response.json();
    })
    .then((data) => {
      const projectDetails = document.getElementById("projectDetails");
      projectDetails.innerHTML = `<h2>${data.name}</h2><p>${data.description}</p>`;
      document.getElementById("addProjectForm").style.display = "none"; // Oculta el formulario si está visible
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("projectDetails").innerHTML =
        "<h2>Proyecto no encontrado</h2><p>Descripción no disponible.</p>";
    });
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
      document.getElementById("projectDescription").value;
    const projectGrid = document.querySelector(".projects-grid");

    // Crear una nueva tarjeta de proyecto
    const newProjectCard = document.createElement("div");
    newProjectCard.setAttribute("data-id", newProjectName); // Usa data-id en lugar de id
    newProjectCard.classList.add("project-card");
    newProjectCard.innerHTML = `<span class="project-title">${newProjectName}</span><p class="project-description">${newProjectDescription}</p>`;

    // Asignar funcionalidad a la nueva tarjeta de proyecto
    newProjectCard.addEventListener("click", function (event) {
      event.preventDefault();
      fetchProjectDetails(newProjectName); // Usa la función para obtener detalles desde el servidor
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
