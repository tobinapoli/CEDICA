function togglePasswordVisibility() {
    const passwordInput = document.getElementById("exampleInputPassword1");
    const toggleEye = document.getElementById("toggleEye");

    if (passwordInput.type === "password") {
        passwordInput.type = "text"; 
        toggleEye.classList.remove("bi-eye"); 
        toggleEye.classList.add("bi-eye-slash"); 
    } else {
        passwordInput.type = "password"; 
        toggleEye.classList.remove("bi-eye-slash"); 
        toggleEye.classList.add("bi-eye"); 
    }
}