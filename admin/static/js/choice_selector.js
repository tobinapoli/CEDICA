
$(document).ready(function() {
    $('#empleado').select2({
        placeholder: ' Seleccione un Empleado ',
        allowClear: true,
        language: {
            noResults: function() {
                return "No se encontraron resultados"; 
            }
        }
    });
});


$(document).ready(function() {
    $('#jinetes').select2({
        placeholder: ' Seleccione un J&A ',
        allowClear: true,
        language: {
            noResults: function() {
                return "No se encontraron resultados"; 
            }
        }
    });
});
