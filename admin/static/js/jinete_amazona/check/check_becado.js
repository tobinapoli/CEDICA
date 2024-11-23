import { toggle_create_jinete_button } from "../toggle/toggle_create_jinete_button.js";

function check_becado() {
    const becadoSelect = document.getElementById('becado');
    const becadoError = document.getElementById('becado-error');

    if (becadoSelect.value === "False") { 
        becadoError.textContent = "";
        return false;
    } else {
        becadoError.textContent = "";
        return true;
    }
}

const becadoSelect = document.getElementById('becado');
becadoSelect.addEventListener('change', check_becado);
becadoSelect.addEventListener('change', toggle_create_jinete_button);

export { check_becado };
