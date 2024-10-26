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
  