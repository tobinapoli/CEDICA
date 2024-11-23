from functools import wraps
from flask import session
from functools import wraps
from flask import abort
from src.core.auth.user import User 

def is_authenticated(session):
    """
    Verifica si el usuario está autenticado.

    Parámetros:
    -----------
    - session: La sesión del usuario actual.

    Retorna:
    --------
    - bool: True si el usuario está autenticado; False en caso contrario.
    """
    return session.get('user') is not None or "google_id" in session

def login_required(func):
    """
    Decorador que asegura que el usuario esté autenticado.

    Si el usuario no está autenticado, aborta la solicitud con un error 401.

    Parámetros:
    -----------
    - func: La función que se va a decorar.

    Retorna:
    --------
    - function: La función decorada.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated(session):
            abort(401)
        return func(*args, **kwargs)
    return wrapper

def check_permission(permission):
    """
    Decorador que verifica si el usuario tiene el permiso especificado.

    Parámetros:
    -----------
    - permission (str): El permiso que se va a verificar.

    Retorna:
    --------
    - function: La función decorada si el usuario tiene el permiso; 
                de lo contrario, aborta con un error 403.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if "google_id" in session:
                user_Aux = session.get('email')
            else:
                user_Aux = session.get('user') 
            user = User.get_by_email(user_Aux) 
            if user is None:
                abort(401) 
            user_permissions = user.get_permission()
            if permission not in user_permissions:
                abort(403)  
            return func(*args, **kwargs)  
        return wrapper
    return decorator