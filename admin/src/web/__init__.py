from flask import Flask
from flask_wtf import CSRFProtect
from flask_cors import CORS
from src.core.config import config
from src.core import database
from src.core.bcrypt import bcrypt
from flask_session import Session
from src.web import comandos
from src.web import rutas
from src.web import errores
from src.web import funciones_jinja 
from flask_cors import CORS
from src.web.storage import storage
session = Session()


csrf = CSRFProtect()


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    # Cargando configuracion
    app.config.from_object(config[env])
    # Inicio CORS                                                                              
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:4173","https://grupo46.proyecto2024.linti.unlp.edu.ar", "https://admin-grupo46.proyecto2024.linti.unlp.edu.ar", "http://localhost:5174"]}})
    # Inicio base de datos
    database.init_app(app)
    # Inicio la sesion
    session.init_app(app)
    # Inicio bcrypt
    bcrypt.init_app(app)
    # Registro rutas
    rutas.register(app) 
    # Registro el storage
    storage.init_app(app)
    # Registro de manejadores de errores
    errores.register(app)
    # Registrar funciones de jinja
    funciones_jinja.register(app)


    # Comandos de flask
    comandos.register(app)

    app.config['WTF_CSRF_ENABLED'] = False


    return app