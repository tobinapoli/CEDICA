from src.web.handlers.auth import is_authenticated
from src.web.controllers.auth import check_role
from src.web.controllers.auth import user_has_role
def register(app):
    app.jinja_env.globals.update(is_authenticated=is_authenticated)
    app.jinja_env.globals.update(check_role=check_role)
    app.jinja_env.globals.update(user_has_role=user_has_role)
    