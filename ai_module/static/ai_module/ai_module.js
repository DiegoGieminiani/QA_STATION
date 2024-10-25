function mostrarLoader() {
    document.getElementById('loading').style.display = 'block';
}

// Función para mostrar el icono de carga
function mostrarLoader() {
    document.getElementById("loading").style.display = "block";
}

// Función para enviar JSON al presionar el botón
function enviarJSON() {
    fetch("{% url 'enviar_json' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        }
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