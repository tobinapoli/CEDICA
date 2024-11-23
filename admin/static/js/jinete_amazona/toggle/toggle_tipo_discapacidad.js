import { check_certificado } from "../check/check_certificado.js";

function toggle_tipo_discapacidad() {
    const tipoSelect = document.getElementById("tipo_discapacidad");

    if (check_certificado() === false) {
        tipoSelect.disabled = true;
        tipoSelect.value = ""; // Limpia el valor si se desactiva
    } else {
        tipoSelect.disabled = false;
    }
}

const certificadoSelect = document.getElementById('certificado_discapacidad');
certificadoSelect.addEventListener('change', toggle_tipo_discapacidad);

toggle_tipo_discapacidad()

export { toggle_tipo_discapacidad };
