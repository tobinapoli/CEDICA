from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import session
from flask import url_for
from src.core import auth
from functools import wraps
from flask import abort
from src.core.auth.user import User 
import requests
from google.oauth2 import id_token
import google.auth.transport.requests


import cachecontrol



bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.get("/")
def login():
    """
    Renderiza la página de inicio de sesión.

    Retorna:
    --------
    - str: Renderiza la plantilla "auth/login.html".
    """
    return render_template("auth/login.html")



@bp.get("/confirmacion")
def confirmacion():
    """
    Renderiza la página de confirmación de registro.

    Retorna:
    --------
    - str: Renderiza la plantilla "auth/confirmacion.html".
    """
    return render_template("auth/confirmacion.html")

@bp.post("/authenticate")
def authenticate():
    """
    Autentica al usuario basado en las credenciales proporcionadas.

    Valida el correo electrónico y la contraseña del usuario. Si son correctos, 
    se guarda el correo en la sesión. De lo contrario, se muestra un mensaje de error.

    Retorna:
    --------
    - str: Redirige a la página de inicio si la autenticación es exitosa; 
           de lo contrario, redirige a la página de inicio de sesión.
    """
    params = request.form
    user = auth.check_user(params.get('email'), params.get('password'))
    if not user:
        flash("Usuario o contraseña incorrectos", "error")
        return redirect(url_for("auth.login"))
    session['user'] = user.email
    flash("¡La sesion se inicio correctamente!", "success")
    return redirect(url_for("home"))

@bp.get("/google_login")
def googleLogin():
    """
    Inicia el proceso de autenticación con Google para el inicio de sesión.

    Este endpoint redirige al usuario a la página de inicio de sesión de Google, donde puede autorizar
    la aplicación para acceder a su información. La URL de redirección después de la autorización se
    configura a partir de la configuración de la aplicación.

    - `GET`: Redirige al usuario a la URL de autorización de Google para iniciar sesión.

    Redirección:
    - El usuario será redirigido a Google para iniciar sesión y autorizar la aplicación.
    - Una vez que el usuario autorice la aplicación, será redirigido a la URL especificada en la configuración de la aplicación.

    Ejemplo de redirección:
    - Redirige a la URL de Google con los parámetros de autorización para iniciar sesión.

    """
    from flask import current_app
    flow = auth.get_flow()
    authorization_url, state = flow.authorization_url()
    session['login_state'] = state
    print(current_app.config.get("GOOGLE_REDIRECT_URI"))
    flow.redirect_uri = current_app.config.get("GOOGLE_REDIRECT_URI")
    return redirect(authorization_url)

@bp.get("/google_register")
def googleRegister():
    """
    Inicia el proceso de autenticación con Google para el registro de usuario.

    Este endpoint redirige al usuario a la página de autorización de Google, donde puede autorizar
    la aplicación para registrar un nuevo usuario. La URL de redirección después de la autorización
    se configura a partir de la configuración de la aplicación.

    - `GET`: Redirige al usuario a la URL de autorización de Google para registrar una cuenta.

    Redirección:
    - El usuario será redirigido a Google para autorizar el registro.
    - Tras autorizar la aplicación, será redirigido a la URL especificada en la configuración de la aplicación.

    Ejemplo de redirección:
    - Redirige a la URL de Google con los parámetros de autorización para el registro de usuario.

    """
    from flask import current_app
    flow_register = auth.get_flow_register()
    authorization_url, state = flow_register.authorization_url()
    session['register_state'] = state
    print(current_app.config.get("GOOGLE_REDIRECT_URI_REGISTER"))
    flow_register.redirect_uri = current_app.config.get("GOOGLE_REDIRECT_URI_REGISTER")
    return redirect(authorization_url)

@bp.get("/callback")
def callback():
    """
    Callback para completar el proceso de inicio de sesión con Google.

    Este endpoint se encarga de manejar la respuesta de Google después de que el usuario autoriza la aplicación.
    Verifica si hay algún error durante el proceso de autenticación y maneja el flujo de obtención de token
    para autenticar al usuario.

    - Si el acceso es denegado, muestra un mensaje de advertencia y redirige al usuario a la página de login.
    - Si la autenticación es exitosa, valida la identidad del usuario mediante el id_token de Google y establece
      las variables de sesión correspondientes.
    - Si el usuario está registrado y su registro está aprobado, se inicia la sesión correctamente y se redirige
      al usuario a la página principal.
    - Si el usuario no está registrado o su registro no está aprobado, se redirige al login con un mensaje de error.

    Métodos:
    - `GET`: Recibe la respuesta de Google después de que el usuario autoriza la aplicación.

    Parámetros de URL:
    - `error`: Si el valor es "access_denied", significa que el usuario denegó el acceso.
    - `state`: Verifica que el estado de la sesión coincida con el que fue enviado por Google.

    Redirecciones:
    - En caso de éxito, redirige al usuario a la página principal (`home`).
    - En caso de error o acceso denegado, redirige al usuario a la página de login.

    Excepciones:
    - Si ocurre algún error durante el proceso, se limpia la sesión y se redirige al login.

    """
    from flask import current_app
    try:
        # Verificar si el error es "access_denied"
        error = request.args.get('error')
        if error == 'access_denied':
            flash("Acceso denegado. No se pudo completar el inicio de sesión.", "warning")
            session.pop('login_state', None)
            return redirect(url_for('auth.login'))
        
        flow = auth.get_flow()
        flow.fetch_token(authorization_response=request.url)
        if session.get('login_state') != request.args.get('state'):
            session.clear()
            abort(500)
        
        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session = cached_session)
        
        id_info = id_token.verify_oauth2_token(
            id_token = credentials.id_token, 
            request = token_request, 
            audience = current_app.config.get("GOOGLE_CLIENT_ID")
            )
        
        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        session["google_token"] = credentials.token
        session["email"] = id_info.get("email")
        user = auth.check_google_user(session.get('email'))
        if not user or not user.registroAprobado:
            session.clear()
            flash("Usuario no registrado", "error")
            return redirect(url_for("auth.login"))
        flash("¡La sesion se inicio correctamente!", "success")
        return redirect(url_for("home"))
    except Exception as e:
        session.clear()
        flash("Acceso denegado. No se pudo completar el inicio de sesión.", "warning")
        return redirect(url_for('auth.login'))  # Redirigir a la página de login
    
    
@bp.get("/register_callback")
def register_callback():
    """
    Callback para completar el proceso de registro de usuario con Google.

    Este endpoint maneja la respuesta de Google después de que el usuario autoriza la aplicación para el registro.
    Obtiene el token de acceso, verifica el id_token y registra al usuario en la base de datos si es necesario.

    - Si el usuario ya está registrado, muestra un mensaje de error indicando que el correo ya está en uso.
    - Si el registro es exitoso, registra al nuevo usuario y redirige a la página de confirmación.
    - En caso de error durante el proceso de registro, se limpia la sesión y redirige al login con un mensaje de advertencia.

    Métodos:
    - `GET`: Recibe la respuesta de Google después de la autorización.

    Parámetros de URL:
    - `state`: Verifica que el estado de la sesión coincida con el enviado por Google.

    Redirecciones:
    - En caso de éxito, redirige al usuario a la página de confirmación.
    - En caso de error, redirige al usuario al login con un mensaje de advertencia o error.

    Excepciones:
    - Si el correo electrónico ya está registrado, muestra un mensaje de error.
    - Si ocurre un error en cualquier parte del proceso, muestra un mensaje de advertencia.

    """
    from flask import current_app
    try:
        flow_register = auth.get_flow_register()
        flow_register.fetch_token(authorization_response=request.url)
        if session.get('register_state') != request.args.get('state'):  # Validar 'register_state'}
            session.clear()
            abort(500)
        
        credentials = flow_register.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session = cached_session)
        
        id_info = id_token.verify_oauth2_token(
            id_token = credentials.id_token, 
            request = token_request, 
            audience = current_app.config.get("GOOGLE_CLIENT_ID")
            )
        
        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        session["google_token"] = credentials.token
        session["email"] = id_info.get("email")
        
        
        User.register_google_user(id_info)
        session.pop('register_state', None)
        session.clear()   
        return redirect(url_for("auth.confirmacion"))
    except ValueError:
        session.clear()
        flash("El correo electrónico ya está registrado", "error")
        return redirect(url_for('auth.login'))
    except Exception as e:
        session.clear()
        flash("Registro cancelado, intentalo nuevamente.", "warning")
        return redirect(url_for('auth.login'))



@bp.get("/logout")
def logout():
    """
    Finaliza la sesión del usuario y redirige a la página de inicio de sesión.

    Retorna:
    --------
    - str: Redirige a la página de inicio de sesión.
    """
    if session.get('user'):
        del session['user']
        session.clear()
        flash("Sesión finalizada correctamente", "info")
    elif session.get('google_id'):# Comprobar si hay una sesión de Google
        session.clear()
        flash("Sesión finalizada correctamente", "info")

        # Revocar token de Google
        google_logout_url = "https://accounts.google.com/o/oauth2/revoke"
        token = session.pop('google_token', None)  # Recuperar y eliminar el token

        if token:
            try:
                requests.post(google_logout_url, params={'token': token})
                flash("Sesión de Google finalizada correctamente", "info")
            except Exception as e:
                flash("Error al cerrar sesión en Google", "error")
    else:
        flash("No hay ninguna sesión iniciada", "error")
    
    return redirect(url_for("auth.login"))


def check_role(required_role):
    """
    Decorador que verifica si el usuario tiene el rol requerido.

    Parámetros:
    -----------
    - required_role (str): El rol que se va a verificar.

    Retorna:
    --------
    - function: La función decorada si el usuario tiene el rol requerido; 
                de lo contrario, aborta con un error 403.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "google_id" in session:
                user_Aux = session.get('email')
            else:
                user_Aux = session.get('user')  # devuelve el mail de la persona loggeada
            user = User.get_by_email(user_Aux)  # type: ignore

            if user is None:
                abort(401) 

            if user.role.nombre != required_role:  
                abort(403)

            return func(*args, **kwargs)  
        return wrapper
    return decorator

def user_has_role(required_role):
    """
    Verifica si el usuario actual tiene un rol específico.

    Parámetros:
    -----------
    - required_role (str): El rol que se va a verificar.

    Retorna:
    --------
    - bool: True si el usuario tiene el rol requerido; False en caso contrario.
    """
    user_Aux = session.get('user')
    if user_Aux is None:
        return False

    user = User.get_by_email(user_Aux)
    if user is None:
        return False

    return user.role.nombre == required_role


