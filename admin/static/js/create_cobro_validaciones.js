function check_observaciones() {
    const observacionesInput = document.getElementById('observaciones');
    const charCount = document.getElementById('charCount');
    const observaciones = observacionesInput.value;
    const maxLength = 50;
    
    const currentLength = observaciones.length;
    charCount.textContent = `${currentLength}/${maxLength}`;

    if (currentLength > maxLength) {
        observacionesInput.value = observaciones.slice(0, maxLength);
        charCount.textContent = `${maxLength}/${maxLength}`;
    }

    // Cambiar color a rojo si llega al límite
    if (currentLength >= maxLength) {
        charCount.style.color = "red";
    } else {
        charCount.style.color = "inherit"; // Color por defecto
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const observacionesInput = document.getElementById('observaciones');
    
    observacionesInput.addEventListener('input', check_observaciones);
});

function check_monto() {
    const montoInput = document.getElementById('monto');
    const monto = montoInput.value;

    if (monto.length > 9) {
        montoInput.value = monto.slice(0, 9); 
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const montoInput = document.getElementById('monto');
    
    montoInput.addEventListener('input', check_monto);
});

document.getElementById('fechaMin').addEventListener('input', function() {
    var fechaMin = this.value;
    var fechaMaxInput = document.getElementById('fechaMax');

    if (fechaMin) {
        fechaMaxInput.min = fechaMin; // Actualizar el mínimo de fechaMax
        // Si la fechaMax actual es anterior a la nueva fechaMin, actualizarla
        if (fechaMaxInput.value < fechaMin) {
            fechaMaxInput.value = fechaMin;
        }
    } else {
        fechaMaxInput.min = '1994-01-01'; // Restablecer al valor predeterminado
    }
});