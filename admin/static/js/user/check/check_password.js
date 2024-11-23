
function check_password(){
    const passwordInput = document.getElementById('password');
    const passwordError = document.getElementById('password-error');
    const password = passwordInput.value;
      
    if (password.length < 8) {
      passwordError.textContent = "La contraseña debe tener al menos 8 caracteres.";
      passwordError.style.color = "red"; 
      return false
    } else if (!/\d/.test(password)) {
      passwordError.textContent = "La contraseña debe contener al menos un número.";
      passwordError.style.color = "red"; 
      return false
    } else {
      passwordError.textContent = "Contraseña válida";
      passwordError.style.color = "green"; 
      return true
    }
  }
  
  const passwordInput = document.getElementById('password');
  passwordInput.addEventListener('input', check_password);
  
  export {check_password}