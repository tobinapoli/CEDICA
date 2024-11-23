import { check_dni_familiar } from "../check/check_dni_familiar.js";  

import { check_porcentaje_beca } from "../check/check_porcentaje_beca.js"; 

function toggle_create_jinete_button() {
    const submitButton = document.getElementById('submit-button'); 

    if (check_dni_familiar()) {  
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}

export { toggle_create_jinete_button };
