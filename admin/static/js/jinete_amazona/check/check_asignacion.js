function check_asignacion() {
    const asignacionSelect = document.getElementById('asignacion_familiar');
    const asignacionError = document.getElementById('asignacion_familiar-error');

    if (asignacionSelect.value === "False") {
        asignacionError.textContent = "";
        return false;
    } else {
        asignacionError.textContent = "";
        return true;
    }
}

const asignacionSelect = document.getElementById('asignacion_familiar');
asignacionSelect.addEventListener('change', check_asignacion);

export { check_asignacion };
