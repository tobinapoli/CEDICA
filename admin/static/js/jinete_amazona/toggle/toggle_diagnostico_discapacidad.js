import { check_certificado } from "../check/check_certificado.js";

function toggle_diagnostico_discapacidad() {
    const diagnosticoSelect = document.getElementById("diagnostico_discapacidad");
    const diagnosticoOtroContainer = document.getElementById("diagnostico_otro_container"); // El contenedor del campo "OTRO"

    if (check_certificado() === false) {
        diagnosticoSelect.disabled = true;
        diagnosticoSelect.value = ""; // Limpia el valor si se desactiva
        if (diagnosticoOtroContainer) {
            diagnosticoOtroContainer.style.display = "none"; // Oculta el campo adicional si existe
        }
    } else {
        diagnosticoSelect.disabled = false;

        // Controlar si se selecciona "OTRO"
        if (diagnosticoSelect.value === "OTRO") {
            diagnosticoOtroContainer.style.display = "block"; // Muestra el campo adicional
        } else {
            diagnosticoOtroContainer.style.display = "none"; // Oculta el campo si no es "OTRO"
        }
    }
}

toggle_diagnostico_discapacidad()

const certificadoSelect = document.getElementById('certificado_discapacidad');
certificadoSelect.addEventListener('change', toggle_diagnostico_discapacidad);

const diagnosticoSelect = document.getElementById("diagnostico_discapacidad");
diagnosticoSelect.addEventListener('change', toggle_diagnostico_discapacidad); // Escuchar el cambio en el select de diagnóstico

export { toggle_diagnostico_discapacidad };
