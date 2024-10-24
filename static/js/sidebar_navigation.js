document.addEventListener('DOMContentLoaded', function () {
    const sidebarLinksLeft = document.querySelectorAll('.sidebar-left ul li a');
    const sidebarLinksRight = document.querySelectorAll('.sidebar-right ul li a');

    // Función para eliminar 'active' de todos los enlaces
    const removeActiveClass = (links) => {
        links.forEach(link => link.classList.remove('active'));
    };

    // Función para añadir 'active' al enlace correspondiente
    const addActiveClass = (link) => {
        link.classList.add('active');
    };

    // Función para manejar el click en los enlaces del sidebar
    const handleSidebarLinks = (sidebarLinks) => {
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function (event) {
                event.preventDefault(); // Evita el salto predeterminado
                const targetId = this.getAttribute('href').substring(1); // Obtiene el ID de la sección
                const targetSection = document.getElementById(targetId);

                // Desplazamiento suave
                if (targetSection) {
                    window.scrollTo({
                        top: targetSection.offsetTop - 80, // Ajuste para evitar superposición con el navbar
                        behavior: 'smooth'
                    });
                }

                // Marca el enlace como activo
                removeActiveClass(sidebarLinks);
                addActiveClass(this);
            });
        });
    };

    // Aplicar la funcionalidad tanto al sidebar izquierdo como al derecho si existen
    if (sidebarLinksLeft.length > 0) {
        handleSidebarLinks(sidebarLinksLeft);
    }
    if (sidebarLinksRight.length > 0) {
        handleSidebarLinks(sidebarLinksRight);
    }
});
