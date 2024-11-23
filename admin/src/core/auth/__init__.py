from src.core.auth.user import User
from src.core.bcrypt import bcrypt
from google_auth_oauthlib.flow import Flow




def list_user():
    """
    Obtiene la lista de todos los usuarios en la base de datos.

    Retorna:
    --------
    - list: Una lista de instancias de usuario.
    """
    users = User.query.all()
    return users

def find_user_by_email(email):
    """
    Busca un usuario en la base de datos por su dirección de correo electrónico.

    Parámetros:
    -----------
    - email (str): La dirección de correo electrónico del usuario a buscar.

    Retorna:
    --------
    - User o None: La instancia del usuario si se encuentra, de lo contrario None.
    """
    users = User.query.filter_by(email=email).first()
    return users

def check_user(email, password):
    """
    Verifica las credenciales de un usuario (correo electrónico y contraseña).

    Parámetros:
    -----------
    - email (str): La dirección de correo electrónico del usuario.
    - password (str): La contraseña del usuario.

    Retorna:
    --------
    - User o None: La instancia del usuario si las credenciales son válidas, de lo contrario None.
    """
    user = find_user_by_email(email)
    
    if user:
        # Si el usuario usa Google para autenticarse, no verificar la contraseña
        if user.esUsuarioGoogle:
            return None
        
        # Si la contraseña es None (nullable), no la verificamos
        if user.password is None:
            return None
        
        # Verificar la contraseña con bcrypt si no es None
        if bcrypt.check_password_hash(user.password, password):
            return user
    
    return None


def check_google_user(email):
    """
    Verifica si un usuario de Google ya existe en la base de datos.

    Parámetros:
    -----------
    - email (str): La dirección de correo electrónico del usuario.

    Retorna:
    --------
    - User o None: La instancia del usuario si ya existe, de lo contrario None.
    """
    user = find_user_by_email(email)
    return user

def get_client_secrets_dict():
    from flask import current_app
    """
    Obtiene las credenciales del cliente de Google.

    Retorna:
    --------
    - dict: Las credenciales del cliente de Google.
    """
    return {
        "web": {
            "client_id": current_app.config.get("GOOGLE_CLIENT_ID"),
            "project_id": "proyecto-de-software-grupo46",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": current_app.config.get("GOOGLE_CLIENT_SECRET"),
            "redirect_uris": [
                current_app.config.get("GOOGLE_REDIRECT_URI"), 
                current_app.config.get("GOOGLE_REDIRECT_URI_REGISTER")
            ]
        }
    }

def get_flow():
    from flask import current_app
    """
    Obtiene el flujo de autenticación de Google.

    Retorna:
    --------
    - Flow: El flujo de autenticación de Google.
    """
    client_secrets_dict = get_client_secrets_dict()
    return Flow.from_client_config(
        client_config=client_secrets_dict,  
        scopes=["https://www.googleapis.com/auth/userinfo.profile", 
                "https://www.googleapis.com/auth/userinfo.email", 
                "openid"],
        redirect_uri=current_app.config.get("GOOGLE_REDIRECT_URI")
    )
def get_flow_register():
    from flask import current_app
    """
    Obtiene el flujo de autenticación de Google para el registro.

    Retorna:
    --------
    - Flow: El flujo de autenticación de Google para el registro.
    """
    client_secrets_dict = get_client_secrets_dict()
    return Flow.from_client_config(
        client_config=client_secrets_dict,  
        scopes=["https://www.googleapis.com/auth/userinfo.profile", 
                "https://www.googleapis.com/auth/userinfo.email", 
                "openid"],
        redirect_uri=current_app.config.get("GOOGLE_REDIRECT_URI_REGISTER")
    )
