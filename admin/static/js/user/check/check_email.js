
function check_email(){
  const emailInput = document.getElementById('email');
  const emailError = document.getElementById('email-error'); 
  const email = emailInput.value;

  if (email.indexOf('@') === -1 || email.indexOf('@') === 0 || email.indexOf('@') === email.length - 1) {
    emailError.textContent = "El correo electrónico debe tener un formato válido.";
    emailError.style.color = "red";
    return false;
  } else if (email.indexOf('.') === -1 || email.indexOf('.') < email.indexOf('@') || email.lastIndexOf('.') >= email.length - 2 || email.length - email.lastIndexOf('.') > 5) {
    emailError.textContent = "El dominio del correo electrónico debe tener un formato válido.";
    emailError.style.color = "red";
    return false;
  } else {
    emailError.textContent = "email valido";
    emailError.style.color = "green";
    return true;
  }
}

const emailInput = document.getElementById('email');
emailInput.addEventListener('input', check_email);

export { check_email }