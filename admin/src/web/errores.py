from src.web.handlers import error

def register(app):
    app.register_error_handler(404, error.error_404)
    app.register_error_handler(401, error.error_401)
    app.register_error_handler(403, error.error_403)
    app.register_error_handler(400, error.error_integrity)
    app.register_error_handler(500, error.error_programming)
    app.register_error_handler(501, error.error_statement)
    