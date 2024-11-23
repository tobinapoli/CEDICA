function check_alias() {
    const aliasInput = document.getElementById('alias');
    const aliasError = document.getElementById('alias-error');
    const alias = aliasInput.value.trim();
  
    if (alias.length < 3) {
      aliasError.textContent = "El nombre debe tener al menos 3 caracteres.";
      aliasError.style.color = "red";
      return false;
    } else {
      aliasError.textContent = "";
      return true;
    }
  }
  
  const aliasInput = document.getElementById('alias');
  aliasInput.addEventListener('input', check_alias);
  
  export { check_alias };