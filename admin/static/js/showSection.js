function showSection(section) {
    // Oculta todas las secciones
    document.getElementById('section-info').style.display = 'none';
    document.getElementById('section-docs').style.display = 'none';
    document.getElementById('section-familiares').style.display = 'none';

    // Muestra la sección seleccionada
    document.getElementById('section-' + section).style.display = 'block';

    // Resalta el botón activo
    const buttons = document.querySelectorAll('.btn-group .btn');
    buttons.forEach(btn => {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-secondary');
    });
    document.getElementById('btn-' + section).classList.remove('btn-secondary');
    document.getElementById('btn-' + section).classList.add('btn-primary');
}
