
function check_telefono() {
    const telefonoInput = document.getElementById('telefono');
    const telefonoError = document.getElementById('telefono-error');
    

    const telefonoRegex = /^[0-9]+$/;

    if (!telefonoRegex.test(telefonoInput.value)) {
        telefonoError.textContent = "El teléfono solo debe contener números.";
        telefonoError.style.color = "red";  
        telefonoInput.classList.add('is-invalid'); 
        return false;
    } else {
        telefonoError.textContent = "";
        telefonoInput.classList.remove('is-invalid'); 
        return true;
    }
}

document.getElementById('telefono').addEventListener('input', check_telefono);

export { check_telefono };
