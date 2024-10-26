function mostrarLoader() {
    document.getElementById('loading').style.display = 'block';
}

// Función para mostrar el icono de carga
function mostrarLoader() {
    document.getElementById("loading").style.display = "block";
}

function enviarJSON() {
    fetch("{% url 'enviar_json' %}", {  // Django procesa la URL en el HTML
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify({ key: "valor" })  // Cambia el JSON según lo que necesites enviar
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("mensaje").innerText = data.mensaje;
    })
    .catch(error => {
        console.error("Error al enviar JSON:", error);
        document.getElementById("mensaje").innerText = "Error al enviar JSON.";
    });
}