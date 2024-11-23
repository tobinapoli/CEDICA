
from flask import redirect, render_template, request, url_for, flash
from flask import Blueprint
from src.web.handlers.auth import check_permission
from src.core import auth
from src.web.handlers.auth import login_required
from src.core.board.rol import Rol
from os import environ
from src.web.controllers.form.user_form import UserCreateForm
from src.web.controllers.form.user_update_form import UserUpdateForm



bp = Blueprint("user", __name__, url_prefix="/usuarios")

@bp.route("/")
@login_required
@check_permission("index_user")
def index(): 
    """
    Renderiza la lista de usuarios con opciones de filtrado, orden y paginación.

    Obtiene los parámetros de consulta (filtros, ordenación y paginación) de 
    la solicitud y devuelve la página de visualización de usuarios con la 
    lista de usuarios filtrada y ordenada.

    Returns:
        Renderiza la plantilla 'user/index.html.jinja' con los usuarios filtrados, 
        roles y detalles de paginación.
    """   
    filters = {
        'email': request.args.get('email', ''),
        'activo': request.args.get('activo', ''),
        'rol': request.args.get('rol', ''), 
        'registroAprobado': request.args.get('registroAprobado', '')

    }
    order_by = request.args.get('ordenar_por', 'alias') 
    order_direction = request.args.get('orden', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = int(environ.get('PAGINATION_PER_PAGE', 25))

    users = auth.User.get_all_users(page=page, filters=filters, order_by=order_by, order_dir=order_direction, per_page=per_page) 
    roles = Rol.get_all_role()  
    
    total_users = auth.User.count_users(filters=filters) 
    total_pages = (total_users // per_page) + (1 if total_users % per_page > 0 else 0)
    
    start = max(1, page - 2)
    end = min(total_pages, page + 2)
    
    return render_template("user/index.html.jinja", users=users, filters=filters, order_by=order_by, order_direction=order_direction, roles=roles, total_pages=total_pages, page=page, start=start, end=end)

@bp.route("/create", methods=["GET", "POST"])  
@login_required
@check_permission("create_user")
def create():
    """
    Maneja la creación de un nuevo usuario.

    Si se recibe una solicitud GET, renderiza el formulario de creación de usuario.
    Si se recibe una solicitud POST, intenta crear un nuevo usuario con los datos 
    del formulario y redirige a la página de usuarios en caso de éxito o vuelve a 
    la creación en caso de error.

    Returns:
        Redirige a 'user.index' si la creación es exitosa. 
        Renderiza 'user/create.html.jinja' con los roles disponibles.
    """

    form = UserCreateForm()
    form.rol_id.choices = [(0, "Seleccione rol")] + [(rol.id, rol.nombre) for rol in Rol.get_all_role()]

    if form.validate_on_submit():
        
        try:
            

            auth.User.create_user(
                email=str(form.data['email']),
                alias=str(form.data['alias']),
                password=str(form.data['password']),
                rol_id=form.data['rol_id']
            )
            flash("Usuario creado exitosamente.", "success")
            return redirect(url_for("user.index"))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("user.create"))
    

    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error en {getattr(form, field).label.text}: {error}", "error")
    
    return render_template("user/create.html.jinja", form=form)

@bp.route("/<user_id>/update", methods=["GET", "POST"])
@login_required
@check_permission("edit_user")
def update(user_id):
    """
    Maneja la actualización de un usuario existente.

    Si se recibe una solicitud GET, renderiza el formulario de actualización de usuario.
    Si se recibe una solicitud POST, intenta actualizar el usuario con los datos del 
    formulario y redirige a la página de usuarios en caso de éxito o vuelve a la 
    actualización en caso de error.

    Args:
        user_id (str): ID del usuario a actualizar.

    Returns:
        Redirige a 'user.index' si la actualización es exitosa.
        Renderiza 'user/update.html.jinja' con los datos del usuario y los roles disponibles.
    """
    user = auth.User.get_user(user_id)
    
    if(not user.registroAprobado):
        flash("El usuario no existe", "error")
        return redirect(url_for("user.index"))
    rol = Rol.get_all_role()
    form = UserUpdateForm()
    form.rol_id.choices = [(rol.id, rol.nombre) for rol in Rol.query.all()]

    # Lógica para verificar si el usuario es de Google, usando user.esUsuarioGoogle
    is_google_user = user.esUsuarioGoogle

    if request.method == 'POST':
        if form.validate_on_submit():
            new_data = {}

            # Si no es un usuario de Google, permitimos cambios en el email, alias y contraseña
            if not is_google_user:
                if form.new_email.data:
                    new_data["new_email"] = form.new_email.data
                if form.alias.data:
                    new_data["alias"] = form.alias.data
                if form.password.data:
                    new_data["password"] = form.password.data

            # Siempre permitimos cambios en el rol y el estado de activo
            if form.activo.data is not None:
                new_data["activo"] = form.activo.data
            if form.rol_id.data:
                new_data["rol_id"] = form.rol_id.data

            try:
                auth.User.update_user(user.id, new_data)
                flash("Usuario actualizado correctamente", "success")
                return redirect(url_for("user.index", user_id=user.id))
            except ValueError as e:
                flash(str(e), "error")
                return redirect(url_for("user.update", user_id=user.id))

    return render_template("user/update.html.jinja", form=form, user=user, roles=rol, is_google_user=is_google_user)





@bp.route("/<user_id>/delete", methods=["GET", "POST"]) 
@login_required
@check_permission("delete_user")
def delete(user_id):
    """
    Maneja la eliminación de un usuario.

    Si se recibe una solicitud POST, intenta eliminar el usuario especificado 
    y redirige a la página de usuarios con un mensaje de éxito o error.

    Args:
        user_id (str): ID del usuario a eliminar.

    Returns:
        Redirige a 'user.index' después de la eliminación del usuario.
    """
    user = auth.User.get_user(user_id)
    if request.method == 'POST':
        try:
            user.delete_user()
            flash("Usuario eliminado correctamente", "success")
        except ValueError as e:
            flash(str(e), "error")    
        finally:    
            return redirect(url_for("user.index"))

@bp.route("/show/<int:user_id>", methods=["GET"])
@login_required
@check_permission("view_user")
def show(user_id):
    """
    Muestra la información de un usuario específico.

    Renderiza una página de detalles del usuario con la información del usuario 
    especificado y su rol.

    Args:
        user_id (int): ID del usuario a mostrar.

    Returns:
        Renderiza la plantilla 'user/show.html.jinja' con los datos del usuario y su rol.
    """
    user = auth.User.get_user(user_id)
    if not user.registroAprobado:
        flash("El usuario no existe", "error")
        return redirect(url_for("user.index"))
    rol = Rol.query.get(user.rol_id)
    return render_template("user/show.html.jinja", user=user, rol=rol)


@bp.route("/user/completar_registro/<int:user_id>", methods=["GET", "POST"])
@login_required
@check_permission("accept_user")
def completar_registro(user_id):
    """
    Completa el registro de un usuario asignándole un rol.

    Este endpoint permite a un usuario administrador completar el registro de un usuario pendiente
    asignándole un rol. Está protegido por un decorador de permisos, lo que asegura que solo los
    usuarios con el permiso adecuado puedan ejecutar esta acción.

    - `user_id`: ID del usuario que se va a actualizar.
    - `GET`: Devuelve el formulario para seleccionar el rol del usuario.
    - `POST`: Procesa el formulario, valida los datos y actualiza el rol del usuario.

    Si el formulario se envía correctamente:
    - Se asigna el nuevo rol al usuario.
    - Se marca el campo `registroAprobado` como `True`.

    Respuestas:
    - Si el rol se asigna correctamente, el usuario es redirigido a la página de la lista de usuarios con un mensaje de éxito.
    - Si ocurre un error, el formulario se vuelve a renderizar con un mensaje de error.

    Ejemplo de respuesta:
    - **Redirect** a la página de la lista de usuarios o **renderizado** del formulario de registro.

    Parámetros:
    - `user_id`: El ID del usuario cuyo registro será completado y rol asignado.

    Excepciones:
    - Si ocurre un error en el proceso de asignación de rol o actualización, se muestra un mensaje de error.

    """
    user = auth.User.get_user(user_id)
    roles = [rol for rol in Rol.get_all_role() if rol.nombre != "System Admin"]  # Excluir SystemAdmin
    form = UserUpdateForm()
    
    # Llenar las opciones de rol para el formulario
    form.rol_id.choices = [(rol.id, rol.nombre) for rol in roles]
    
    if request.method == 'POST':
        if form.validate_on_submit():
            # Obtenemos el rol seleccionado
            new_role_id = form.rol_id.data

            # Crear el diccionario con el nuevo rol
            new_data = {
                "rol_id": new_role_id,
                "registroAprobado": True  # Establecer registroAprobado a True automáticamente
            }
            
            try:
                # Asignar el rol y actualizar el usuario
                if user.assign_role(new_role_id):  # Usamos el método assign_role
                    auth.User.update_user(user.id, new_data)
                    flash("Usuario actualizado correctamente y rol asignado.", "success")
                    return redirect(url_for("user.index"))
            except ValueError as e:
                flash(str(e), "error")
                return redirect(url_for("user.update", user_id=user.id))

    return render_template("user/completar_registro.html", form=form, user=user, roles=roles)


