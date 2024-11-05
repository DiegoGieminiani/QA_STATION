document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.querySelector('#toggle-password');
    const passwordField = document.querySelector('#password');
  
    togglePassword.addEventListener('click', function () {
      // Alternar el tipo de input de password a texto
      const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordField.setAttribute('type', type);
      
      // Alternar el ícono de ojo (cambiando entre el ojo y el ojo tachado)
      if (type === 'password') {
        this.classList.add('fa-eye');
        this.classList.remove('fa-eye-slash');
      } else {
        this.classList.add('fa-eye-slash');
        this.classList.remove('fa-eye');
      }
    });
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