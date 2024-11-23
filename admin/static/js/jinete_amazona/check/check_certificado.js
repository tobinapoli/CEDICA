function check_certificado() {
    const certificadoSelect = document.getElementById('certificado_discapacidad');
    const certificadoError = document.getElementById('certificado_discapacidad-error');

    if (certificadoSelect.value === "False") {
        certificadoError.textContent = "";
        return false;
    } else {
        certificadoError.textContent = "";
        return true;
    }
}

const certificadoSelect = document.getElementById('certificado_discapacidad');
certificadoSelect.addEventListener('change', check_certificado);

export { check_certificado };
    