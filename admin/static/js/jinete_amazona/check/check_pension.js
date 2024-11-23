// check_pension.js
function check_pension() {
    const pensionadoSelect = document.getElementById('pensionado');
    const pensionadoError = document.getElementById('pensionado-error');

    if (pensionadoSelect.value === "False") {
        pensionadoError.textContent = "";
        return false;
    } else {
        pensionadoError.textContent = "";
        return true;
    }
}

const pensionadoSelect = document.getElementById('pensionado');
pensionadoSelect.addEventListener('change', check_pension);

export { check_pension };
