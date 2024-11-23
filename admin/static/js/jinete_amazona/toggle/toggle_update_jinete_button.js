import { check_dni_familiar } from "../check/check_dni_familiar.js"; 
import { check_porcentaje_beca } from "../check/check_porcentaje_beca.js"; 

function toggle_update_jinete_button() {
    const submitButton = document.getElementById('update-button'); // Asegúrate de que este ID sea correcto para el botón de actualización

    if (check_dni_familiar() && check_porcentaje_beca()) {  
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}

export { toggle_update_jinete_button };
