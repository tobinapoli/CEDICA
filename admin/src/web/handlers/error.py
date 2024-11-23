from dataclasses import dataclass
from flask import render_template

@dataclass
class Error:
    """
    Clase que representa un error.
    """
    code: int
    message: str    
    description: str

def error_404(e):
    """
    Maneja los errores 404 (No encontrado).

    :param e: Excepción que se ha lanzado (no se utiliza en este contexto).
    :return: Renderiza una plantilla de error con el código y mensaje de error 404.
    """
    error = Error(404, "Not Found", "La url no fue encontrada en el servidor")
    return render_template("error.html", error = error), 404

def error_401(e):
    """
    Maneja los errores 401 (No autorizado).

    :param e: Excepción que se ha lanzado (no se utiliza en este contexto).
    :return: Renderiza una plantilla de error con el código y mensaje de error 401.
    """
    error = Error(401, "Unauthorized", "No estas autorizado para acceder a este recurso")
    return render_template("error.html", error = error), 401

def error_403(e):
    """
    Maneja los errores 403 (Prohibido).

    :param e: Excepción que se ha lanzado (no se utiliza en este contexto).
    :return: Renderiza una plantilla de error con el código y mensaje de error 403.
    """
    error = Error(403, "Forbidden", "No tienes permisos para acceder a este recurso")
    return render_template("error.html", error = error), 403 

def error_integrity(e):
    """
    Maneja los errores de integridad (IntegrityError).
    """
    error = Error(400, "Integrity Error", "Ocurrió un error de integridad en la base de datos.")
    return render_template("error.html", error=error), 400

def error_programming(e):
    """
    Maneja los errores de programación (ProgrammingError).
    """
    error = Error(500, "Programming Error", "Ocurrió un error de programación en la consulta de la base de datos.")
    return render_template("error.html", error=error), 500

def error_statement(e):
    """
    Maneja el error statement (StatementError)    
    """
    error = Error(501, "Oops! Error", "Ocurrió un error")
    return render_template("error.html", error=error), 501