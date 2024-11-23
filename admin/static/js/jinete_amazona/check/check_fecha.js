// check_fecha.js

function check_fecha() {
    const fechaInput = document.getElementById('fecha_nacimiento');
    const fechaError = document.getElementById('fecha_nacimiento-error');

    // Obtener la fecha actual
    const fechaHoy = new Date();
    const fechaMaxima = new Date();
    fechaMaxima.setFullYear(fechaHoy.getFullYear() - 100); // Fecha máxima es 100 años atrás

    // Convertir las fechas al formato YYYY-MM-DD para la comparación
    const fechaHoyStr = fechaHoy.toISOString().split('T')[0];
    const fechaMaximaStr = fechaMaxima.toISOString().split('T')[0];

    if (fechaInput.value > fechaHoyStr) {
        fechaError.textContent = "La fecha no puede ser mayor que hoy.";
        fechaError.style.color = "red";  // Mostrar el error en rojo
        fechaInput.classList.add('is-invalid'); // Añadir clase de error si usas Bootstrap
        return false;
    } else if (fechaInput.value < fechaMaximaStr) {
        fechaError.textContent = "La fecha no puede ser menor a 100 años atrás.";
        fechaError.style.color = "red";
        fechaInput.classList.add('is-invalid');
        return false;
    } else {
        fechaError.textContent = "";
        fechaInput.classList.remove('is-invalid'); // Elimina la clase de error si es válida
        return true;
    }
}

// Exportar la función
export { check_fecha };
