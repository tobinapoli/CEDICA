import { check_email } from "../check/check_email.js";
import { check_password } from "../check/check_password.js";

function toggle_submit_button() {
    const submitButton = document.getElementById('submit-button'); 

    if (check_email() && check_password()) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}
  
export { toggle_submit_button };
