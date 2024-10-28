document.addEventListener("DOMContentLoaded", function () {
  // Código para manejar la activación de los enlaces en el navbar
  const links = document.querySelectorAll(".navbar-links a");

  links.forEach((link) => {
    link.addEventListener("click", function () {
      links.forEach((l) => l.classList.remove("active"));
      this.classList.add("active");
    });
  });

  // Código para manejar el menú desplegable en el perfil de usuario
  const userProfile = document.querySelector(".user-profile");
  const dropdownMenu = document.querySelector(".dropdown-menu");

  // Toggle para mostrar/ocultar el menú
  userProfile.addEventListener("click", function (event) {
    event.stopPropagation(); // Evita que el evento se propague fuera de userProfile
    dropdownMenu.classList.toggle("show-menu");
  });

  // Cerrar el menú si se hace clic fuera de él
  document.addEventListener("click", function (event) {
    if (!userProfile.contains(event.target)) {
      dropdownMenu.classList.remove("show-menu");
    }
  });




});
