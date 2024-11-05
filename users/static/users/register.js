// register.js

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".register-form");
  const password1 = form.querySelector("#id_password1");
  const password2 = form.querySelector("#id_password2");
  const submitButton = form.querySelector(".btn-register");

  // Función para mostrar mensajes de error
  function showError(input, message) {
    const formGroup = input.closest(".form-group");
    const errorDiv = formGroup.querySelector(".error-message");

    if (errorDiv) {
      errorDiv.textContent = message;
    } else {
      const errorMessage = document.createElement("div");
      errorMessage.className = "error-message";
      errorMessage.textContent = message;
      formGroup.appendChild(errorMessage);
    }
  }

  // Función para limpiar mensajes de error
  function clearError(input) {
    const formGroup = input.closest(".form-group");
    const errorDiv = formGroup.querySelector(".error-message");

    if (errorDiv) {
      errorDiv.textContent = "";
    }
  }

  // Validación de coincidencia de contraseñas
  function checkPasswordMatch() {
    if (password1.value !== password2.value) {
      showError(password2, "Las contraseñas no coinciden");
      return false;
    } else {
      clearError(password2);
      return true;
    }
  }

  // Validación de campo vacío
  function checkRequiredFields() {
    let valid = true;
    form.querySelectorAll("input").forEach((input) => {
      if (input.value.trim() === "") {
        showError(input, "Este campo es obligatorio");
        valid = false;
      } else {
        clearError(input);
      }
    });
    return valid;
  }

  // Evento para validar al enviar el formulario
  form.addEventListener("submit", function (event) {
    let isFormValid = checkRequiredFields() && checkPasswordMatch();

    if (!isFormValid) {
      event.preventDefault(); // Evita el envío si el formulario es inválido
    }
  });

  // Evento para verificar la coincidencia de contraseñas en tiempo real
  password1.addEventListener("input", checkPasswordMatch);
  password2.addEventListener("input", checkPasswordMatch);
});
document.addEventListener("DOMContentLoaded", function () {
  // Selecciona todos los mensajes flash
  const messages = document.querySelectorAll(".message");

  messages.forEach((message) => {
    // Desvanece y elimina el mensaje después de 5 segundos
    setTimeout(() => {
      message.style.transition = "opacity 0.5s ease";
      message.style.opacity = "0";
      setTimeout(() => message.remove(), 500); // Remueve el mensaje del DOM
    }, 5000); // 5 segundos
  });
});