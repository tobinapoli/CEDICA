import { check_email } from "../check/check_email.js";
import { check_password } from "../check/check_password.js";
import { check_alias } from "../check/check_alias.js";

function toggle_update_user_button() {
    const submitButton = document.getElementById('submit-button'); 

    if (check_email() && check_alias()) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}
  
export { toggle_update_user_button };
