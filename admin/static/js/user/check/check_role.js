function check_role() {
    const rolSelect = document.getElementById('rol_id');
    const rolError = document.getElementById('rol-error');
  
    if (rolSelect.selectedIndex == 0) {
      rolError.textContent = "Por favor, seleccione un rol.";
      rolError.style.color = "red";
      return false;
    } else {
      rolError.textContent = "";
      return true;
    }
  }
  
  const rolSelect = document.getElementById('rol_id');
  rolSelect.addEventListener('change', check_role);
  
  export { check_role };