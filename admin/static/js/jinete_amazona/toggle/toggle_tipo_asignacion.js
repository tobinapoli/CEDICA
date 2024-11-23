import { check_asignacion } from "../check/check_asignacion.js";

function toggle_tipo_asignacion() {
    const tipoSelect = document.getElementById("tipo_asignacion");

    if (check_asignacion() === false) {
        tipoSelect.disabled = true;
        tipoSelect.value = ""; 
    } else {
        tipoSelect.disabled = false;
    }
}

const asignacionSelect = document.getElementById('asignacion_familiar');
asignacionSelect.addEventListener('change', toggle_tipo_asignacion); 

toggle_tipo_asignacion()

export { toggle_tipo_asignacion };
