from flask_sqlalchemy import SQLAlchemy 


db = SQLAlchemy(session_options={'expire_on_commit': False})

def init_app(app):
    """Iniciliza la base de datos con la aplicación de Flask."""
    db.init_app(app)
    config(app)
    return app

def config(app):
    """Configuración de hooks para la base de datos."""

    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()

    return app

def reset():
    """
    Resetea la base de datos.
    """
    print("Eliminando la base de datos")
    db.drop_all()
    print("Creando la base de datos")
    db.create_all()
    print("Base de datos creada")