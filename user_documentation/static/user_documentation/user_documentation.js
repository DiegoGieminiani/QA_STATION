document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('main .content section');
    const sidebarLinks = document.querySelectorAll('.sidebar ul li a');

    // Función para eliminar 'active' de todos los enlaces
    const removeActiveClass = () => {
        sidebarLinks.forEach(link => link.classList.remove('active'));
    };

    // Función para añadir 'active' al enlace correspondiente
    const addActiveClass = (id) => {
        const link = document.querySelector(`.sidebar ul li a[href="#${id}"]`);
        if (link) {
            link.classList.add('active');
        }
    };

    // Agrega el evento click a cada enlace del sidebar
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault(); // Evita el comportamiento de salto de ancla
            const targetId = this.getAttribute('href').substring(1); // Obtiene el ID del target (sin el #)

            // Desplaza suavemente hacia la sección correspondiente
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                window.scrollTo({
                    top: targetSection.offsetTop - 20, // Ajusta el scroll un poco antes de la sección
                    behavior: 'smooth' // Desplazamiento suave
                });
            }

            // Marca el enlace como activo manualmente
            removeActiveClass();
            this.classList.add('active');
        });
    });

    // Usamos Intersection Observer para observar las secciones
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Cuando una sección es visible, activa el enlace correspondiente
                const sectionId = entry.target.getAttribute('id');
                removeActiveClass();
                addActiveClass(sectionId);
            }
        });
    }, {
        root: null,           // Usa el viewport como root
        rootMargin: '0px',    // Sin margen
        threshold: 0.6        // El 60% de la sección debe ser visible para activarse
    });

    // Observa cada sección
    sections.forEach(section => {
        observer.observe(section);
    });
});
