// check_dni_familiar.js

// Crea un mensaje de error
function createErrorSpan(message) {
    const span = document.createElement('span');
    span.classList.add('error');
    span.textContent = message;
    span.style.color = 'red'; // Cambia el color del texto a rojo
    return span;
}

// Verifica que el DNI tenga exactamente 8 caracteres y que sea un número
function isValidDNI(dni) {
    return dni.length === 8 && !isNaN(dni);
}

// Limpia los mensajes de error del input
function clearErrorMessages(input) {
    const errorSpan = input.parentElement.querySelector('.error');
    if (errorSpan) {
        errorSpan.remove(); // Elimina el mensaje de error si existe
    }
}

// Comprueba la validez de los DNIs de los familiares y el jinete
function check_dni_familiar() {
    const dniInputs = document.querySelectorAll('input[name="dni_familiar[]"]'); // Asegúrate de que este nombre sea correcto
    const dniJineteInput = document.getElementById('dni'); // Asegúrate de que este ID sea correcto
    let isValid = true;

    // Validación de los DNI de los familiares
    dniInputs.forEach(input => {
        const dniValue = input.value.trim(); // Obtener el valor y quitar espacios

        // Limpiar mensajes de error previos
        clearErrorMessages(input);

        // Lógica de validación
        if (!isValidDNI(dniValue)) {
            const errorSpan = createErrorSpan("El DNI debe tener exactamente 8 dígitos.");
            input.insertAdjacentElement('afterend', errorSpan); // Insertar el mensaje justo debajo del input
            isValid = false; // Marcar como no válido si hay un error
        }
    });

    // Validación del DNI del jinete
    if (dniJineteInput) {
        const dniJineteValue = dniJineteInput.value.trim();
        clearErrorMessages(dniJineteInput);

        if (!isValidDNI(dniJineteValue)) {
            const errorSpan = createErrorSpan("El DNI del jinete debe tener exactamente 8 dígitos.");
            dniJineteInput.insertAdjacentElement('afterend', errorSpan); // Insertar el mensaje justo debajo del input
            isValid = false;
        }
    }

    return isValid; // Retornar el estado de validez
}

// Define la función toggle_create_jinete_button
function toggle_create_jinete_button(isValid) {
    const createButton = document.getElementById('create-jinete-button'); // Asegúrate de que este ID sea correcto
    if (createButton) {
        createButton.disabled = !isValid; // Habilita o deshabilita el botón
    }
}

// Espera a que se cargue el documento
document.addEventListener('DOMContentLoaded', () => {
    const dniInputs = document.querySelectorAll('input[name="dni_familiar[]"]');
    const dniJineteInput = document.getElementById('dni'); 

    function validateDNIs() {
        let isValid = check_dni_familiar(); 
        toggle_create_jinete_button(isValid); 
    }

    dniInputs.forEach(input => {
        input.addEventListener('input', validateDNIs);
        // Validar inicialmente
        validateDNIs();
    });

    if (dniJineteInput) {
        dniJineteInput.addEventListener('input', validateDNIs);
        // Validar inicialmente
        validateDNIs();
    }
});

// Exportar la función si es necesario
export { check_dni_familiar };
