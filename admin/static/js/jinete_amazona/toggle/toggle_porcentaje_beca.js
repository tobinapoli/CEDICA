import { check_becado } from "../check/check_becado.js";

function toggle_porcentaje_beca() {
    const porcentajeBecaInput = document.getElementById("porcentaje_beca");

    if (check_becado() === true) {
        porcentajeBecaInput.disabled = false;
    } else {
        porcentajeBecaInput.disabled = true;
        porcentajeBecaInput.value = ""; 
    }
}

toggle_porcentaje_beca();

const becadoSelect = document.getElementById('becado');
becadoSelect.addEventListener('change', toggle_porcentaje_beca); 

export { toggle_porcentaje_beca };
