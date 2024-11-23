import { check_pension } from "../check/check_pension.js";

function toggle_tipo_pension() {
    const tipoSelect = document.getElementById("tipo_pension");

    if (check_pension() === false) {
        tipoSelect.disabled = true;
        tipoSelect.value = ""; // Limpia el valor si se desactiva
    } else {
        tipoSelect.disabled = false;
    }
}

const pensionadoSelect = document.getElementById('pensionado');
pensionadoSelect.addEventListener('change', toggle_tipo_pension);

// Llama a la función para verificar el estado al cargar la página
toggle_tipo_pension();

export { toggle_tipo_pension };