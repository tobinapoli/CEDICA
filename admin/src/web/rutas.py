from flask import render_template
from src.web.controllers.user import bp as user_bp
from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.empleado import bp as emp_bp
from src.web.controllers.pago import bp as pago_bp
from src.web.controllers.jinete_amazona import bp as j_bp
from src.web.controllers.cobros import bp as cobros_bp
from src.web.controllers.ejemplar import bp as ejemplar_bp
from src.web.controllers.documento import bp as documento_bp
from src.web.controllers.familiares_responsables import bp as familiares_bp
from src.web.controllers.graficos import bp as graficos_bp
from src.web.controllers.reportes import bp as reportes_bp
from src.web.api.contenido import bp as contenido_api_bp
from src.web.controllers.contenido import bp as contenido_bp
from src.web.api.contacto import bp as consultas_bp
from src.web.controllers.contacto import bp as consultasfront_bp

def register(app):
    @app.route("/")
    def home():
        return render_template("home.html")
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(emp_bp)
    app.register_blueprint(j_bp)
    app.register_blueprint(pago_bp)
    app.register_blueprint(cobros_bp)
    app.register_blueprint(ejemplar_bp)
    app.register_blueprint(documento_bp)
    app.register_blueprint(familiares_bp)
    app.register_blueprint(graficos_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(contenido_bp)
    app.register_blueprint(contenido_api_bp)
    app.register_blueprint(consultas_bp)
    app.register_blueprint(consultasfront_bp)
    