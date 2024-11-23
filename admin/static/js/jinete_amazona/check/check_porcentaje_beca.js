import { check_becado } from "./check_becado.js";

function check_porcentaje_beca() {
    const porcentaje_becaInput = document.getElementById('porcentaje_beca');
    const porcentaje_becaError = document.getElementById('porcentaje_beca-error');
    const porcentaje_beca = parseInt(porcentaje_becaInput.value, 10);

    if (check_becado() === true) {
        if (porcentaje_beca < 0 || porcentaje_beca > 100) {
            porcentaje_becaError.textContent = "Por favor ingrese un porcentaje entre 0 y 100";
            porcentaje_becaError.style.color = "red"; 
            return false;
        } else if (isNaN(porcentaje_beca)) {
            porcentaje_becaError.textContent = "Por favor ingrese un porcentaje válido.";
            porcentaje_becaError.style.color = "red";
            return false;
        } else {
            porcentaje_becaError.textContent = ""; 
            return true;
        }
    } else {
        return true;
    }
}


const porcentaje_becaInput = document.getElementById('porcentaje_beca');
porcentaje_becaInput.addEventListener('input', check_porcentaje_beca);

export { check_porcentaje_beca };
