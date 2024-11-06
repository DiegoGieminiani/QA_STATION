// Cuando se haga clic en un proyecto
document.querySelectorAll(".project-card").forEach((card) => {
  card.addEventListener("click", function (event) {
    event.preventDefault();
    const projectId = this.getAttribute("data-id"); // Usa el atributo data-id para obtener el ID del proyecto
    fetchProjectDetails(projectId); // Llama a la función para obtener los detalles desde el servidor
  });
});
// Coloca esto en tu archivo JavaScript
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Función para obtener los detalles del proyecto
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
      closeAddProjectForm(); // Oculta el formulario si está visible
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
    openAddProjectForm();
  });

// Función para mostrar el formulario y el overlay
function openAddProjectForm() {
  document.getElementById("addProjectForm").style.display = "block";
  document.getElementById("overlay").style.display = "block";
  document.getElementById("projectDetails").innerHTML = ""; // Oculta cualquier detalle de proyecto cuando el formulario está visible
}

// Función para ocultar el formulario y el overlay
function closeAddProjectForm() {
  document.getElementById("addProjectForm").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}

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

    // Ocultar el formulario y el overlay después de agregar el proyecto
    closeAddProjectForm();
  });

// Función para abrir el modal en modo "Ver Detalles del Proyecto"
function redirectToProject(projectId) {
  window.location.href = `/projects/select/${projectId}/`;
}


// Función para cerrar el modal
function closeProjectModal() {
  document.getElementById("projectModal").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}

// Funciones para mostrar/ocultar el formulario de nuevo proyecto
function openAddProjectForm() {
  document.getElementById("addProjectForm").style.display = "block";
  document.getElementById("overlay").style.display = "block";
}

function closeAddProjectForm() {
  document.getElementById("addProjectForm").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}

// Función para eliminar un proyecto
function deleteProject(projectId) {
  if (confirm("¿Estás seguro de que deseas eliminar este proyecto?")) {
    fetch(`/projects/delete/${projectId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken, // Usa el valor dinámico del token CSRF
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          document
            .querySelector(`.project-card[data-id='${projectId}']`)
            .remove();
        } else {
          alert("Error al eliminar el proyecto.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Error al eliminar el proyecto.");
      });
  }
}
