import { check_email } from "../check/check_email.js";
import { check_password } from "../check/check_password.js";
import { check_alias } from "../check/check_alias.js";
import { check_role } from "../check/check_role.js";

function toggle_create_user_button() {
    const submitButton = document.getElementById('submit-button'); 

    if (check_email() && check_alias() && check_password() && check_role()) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}
  
export { toggle_create_user_button };
