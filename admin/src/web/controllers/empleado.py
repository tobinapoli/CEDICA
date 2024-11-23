from flask import render_template, request, redirect, url_for, flash, jsonify
from flask import Blueprint
from datetime import datetime
from src.core import board
from src.web.handlers.auth import login_required, check_permission
from src.core.auth.user import User
from src.core.board.documento import TipoDocumento, TipoTitular, Documento
from src.web.controllers import documento as documento_controller
from src.core.board.domicilio import TipoProvincia
from src.core.database import db
from os import environ
from src.core.board.contacto_emergencia import contacto_emergencia

bp = Blueprint("empleado", __name__, url_prefix="/empleados")

# List empleados
@bp.route("/", methods=["GET"])
@login_required
@check_permission("index_empleado")
def index():
    """
    Muestra la lista de empleados filtrados y ordenados.

    :return: La página con la lista de empleados, con filtros y opciones de ordenamiento aplicadas.
    """
    filters = {
        'nombre': request.args.get('nombre', ''),
        'apellido': request.args.get('apellido', ''),
        'dni': request.args.get('dni', ''),
        'email': request.args.get('email', ''),
        'puesto': request.args.get('puesto', ''),
    }
    
    page = request.args.get('page', 1, type=int)
    per_page = int(environ.get('PAGINATION_PER_PAGE', 25))
    
    
    order_by = request.args.get('ordenar_por', 'nombre')
    order_direction = request.args.get('orden', 'asc')
    
    empleados = board.Empleado.list_empleado(filters=filters, order_by=order_by, order_direction=order_direction, page=page, per_page=per_page)

    total_pages = empleados.pages
    
    start = max(1, page - 2)
    end = min(total_pages, page + 2)
    
    
    puestos = board.Puesto.get_puestos()
    return render_template("empleado/index.html", empleados=empleados,  page=page, total_pages=total_pages ,filters=filters, order_by=order_by, order_direction=order_direction, puestos=puestos, start=start, end=end)

# Create empleado
@bp.route("/create", methods=["GET", "POST"])
@login_required
@check_permission("create_empleado")
def create():
    """
    Crea un nuevo empleado y maneja el formulario de creación. Si la petición es GET,
    muestra el formulario de creación, y si es POST, crea el empleado con los datos
    proporcionados y valida posibles duplicados en los campos clave.

    :return: La página de creación de empleado o una redirección a la lista de empleados.
    """
    if request.method == "POST":
        # Obtener los datos del formulario
        nombre = request.form["name"]
        apellidos = request.form["apellidos"]
        dni = request.form["dni"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        puesto_id = request.form["puesto"]
        profesion = request.form["profesion"]
        fecha_ingreso = request.form["fecha_ingreso"]
        fecha_egreso = request.form["fecha_egreso"] or None
        obra_social = request.form["obra_social"]
        numero_afiliado = request.form["numero_afiliado"]
        condicion = request.form["condicion"]
        activo = request.form.get("activo")
        if activo == "True":
            activo = True
        else:
            activo = False
            
        usuario_id = request.form.get("usuario")
        
        # Datos del contacto de emergencia
        contacto_nombre = request.form["contacto_nombre"]
        contacto_telefono = request.form["contacto_telefono"]

        # Crear el contacto de emergencia
        contacto = board.contacto_emergencia.create_contacto_emergencia(contacto_emergencia, nombre=contacto_nombre, telefono=contacto_telefono) 
     
        # Datos del domicilio
        calle = request.form["calle"]
        numero = request.form["numero"]
        depto = request.form.get("depto")
        localidad = request.form["localidad"]
        provincia = request.form["provincia"]
        

        # Crear el domicilio
        nuevo_domicilio = board.domicilio.create_domicilio(board.domicilio,
            calle=calle,
            numero=numero,
            depto=depto,
            localidad=localidad,
            provincia=provincia
        )

        # Verificar si los datos están repetidos
        error = check_repetidos(dni, numero_afiliado, email)
        if error:
            flash(error, "error")
            profesiones = get_profesiones()
            puestos = board.Puesto.get_puestos()
            return render_template("empleado/create.html", 
                           form_data=request.form, 
                           puestos=puestos, 
                           profesiones=profesiones,
                           selected_puesto=puesto_id,
                           provincias=TipoProvincia,
                           usuarios_disp = User.get_users_without_empleado(),
                           tipos_docs = TipoDocumento.get_tipo_doc_empleado()
                           )
        
        # Crear el empleado con el ID del contacto de emergencia
        empleado = board.Empleado.create_empleado(
            nombre=nombre,
            apellidos=apellidos,
            dni=dni,
            domicilio=nuevo_domicilio.id,  
            telefono=telefono,
            puesto_id=puesto_id,
            email=email,
            profesion=profesion,
            fecha_ingreso=fecha_ingreso,
            fecha_egreso=fecha_egreso,
            contacto_emergencia_id=contacto.id, 
            obra_social=obra_social,
            numero_afiliado=numero_afiliado,
            condicion=condicion,
            activo=activo,
            user_id=usuario_id if usuario_id else None
        )
        
        # Procesar documentos adjuntos
        dni_documento = request.files.get('dni_documento')
        curriculum_documento = request.files.get('curriculum_documento')
        titulo_documento = request.files.get('titulo_documento')

        if dni_documento:
            documento_controller.create(
                file=dni_documento,
                document_type=TipoDocumento.dni_empleado,
                titular_id=empleado.id,
                tipo_titular=TipoTitular.empleado,
                tipo_entrada="archivo",
            )

        if curriculum_documento:
            documento_controller.create(
                file=curriculum_documento,
                document_type=TipoDocumento.cv_empleado,
                titular_id=empleado.id,
                tipo_titular=TipoTitular.empleado,
                tipo_entrada=False,
            )
        
        if titulo_documento:
            documento_controller.create(
                file=titulo_documento,
                document_type=TipoDocumento.titulo_empleado,
                titular_id=empleado.id,
                tipo_titular=TipoTitular.empleado,
                tipo_entrada="archivo",
            )
        
        flash("Empleado creado exitosamente", "success")
        return redirect(url_for("empleado.index"))
    
    provincias = TipoProvincia
    usuarios_disp = User.get_users_without_empleado()
    profesiones = get_profesiones()
    puestos = board.Puesto.get_puestos()
    tipos_docs = TipoDocumento.get_tipo_doc_empleado()
    return render_template("empleado/create.html", form_data={}, puestos=puestos, profesiones=profesiones, tipos_docs=tipos_docs, usuarios_disp=usuarios_disp,provincias=provincias)

# Update empleado
@bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
@check_permission("edit_empleado")
def update(id):
    """
    Actualiza la información de un empleado existente. Si la petición es GET, 
    muestra el formulario de edición precargado. Si es POST, actualiza el empleado
    con los nuevos datos proporcionados.

    :param id: El ID del empleado a actualizar.
    :return: La página de edición de empleado o una redirección a la lista de empleados.
    """
    empleado = board.Empleado.get_empleado(id)
    
    if not empleado:
        return redirect(url_for("empleado.index"))  # Manejo de error si no existe el empleado

    direccion_emp = board.domicilio.get_domicilio(empleado.domicilio)
    contacto_emp = board.contacto_emergencia.get_contacto_emergencia(empleado.contacto_emergencia_id)
    
    if request.method == "POST":
        # Obtener los datos del formulario
        nombre = request.form.get("name")
        apellidos = request.form.get("apellidos")
        dni = request.form.get("dni")
        domicilio = direccion_emp.id #type: ignore
        email = request.form.get("email")
        telefono = request.form.get("telefono")
        profesion = request.form.get("profesion")
        puesto_id = request.form["puesto"]
        fecha_ingreso = request.form.get("fecha_ingreso")
        fecha_egreso = request.form.get("fecha_egreso") or None
        contacto_emergencia = request.form.get("contacto_emergencia")
        obra_social = request.form.get("obra_social")
        numero_afiliado = request.form.get("numero_afiliado")
        condicion = request.form.get("condicion")
        activo = request.form.get("activo")
        if activo == "True":
            activo = True
        else:
            activo = False
        calle = request.form.get("calle")
        numero = request.form.get("numero")
        depto = request.form.get("depto")
        localidad = request.form.get("localidad")
        provincia = request.form.get("provincia")
        contacto_nombre = request.form.get("contacto_nombre")
        contacto_telefono = request.form.get("contacto_telefono")
        
        error = check_repetidos(dni, numero_afiliado, email, current_id=id)
        if error:
            flash(error, "error")
            profesiones = get_profesiones()
            puestos = board.Puesto.get_puestos()
            return render_template("empleado/update.html", 
                                   empleado=empleado, 
                                   domicilio=direccion_emp, 
                                   contacto=contacto_emp,
                                   puestos=puestos,
                                   profesiones=profesiones,
                                   form_data=request.form)

        # Llamar a la función update_empleado con todos los valores
        board.Empleado.update_empleado(
            id,
            nombre=nombre,
            apellido=apellidos,
            dni=dni,
            domicilio=domicilio,
            telefono=telefono,
            email=email,
            puesto_id=puesto_id,
            profesion=profesion,
            fecha_ingreso=fecha_ingreso,
            fecha_egreso=fecha_egreso,
            contacto_emergencia=contacto_emergencia,
            obra_social=obra_social,
            numero_afiliado=numero_afiliado,
            condicion=condicion,
            activo=activo
        )
        
        board.domicilio.update_domicilio(
            domicilio,
            calle=calle,
            numero=numero,
            depto=depto,
            localidad=localidad,
            provincia=provincia
        )
        
        
        board.contacto_emergencia.update_contacto_emergencia(
            contacto_emp.id, 
            nombre=contacto_nombre,
            telefono=contacto_telefono
        )
        flash("Empleado editado exitosamente", "success")
        return redirect(url_for("empleado.index"))
    
    profesiones = get_profesiones()
    puestos = board.Puesto.get_puestos()
    return render_template("empleado/update.html", empleado=empleado, domicilio=direccion_emp, contacto = contacto_emp, profesiones=profesiones, puestos=puestos, form_data={}, provincias=TipoProvincia)

# Show empleado
@bp.route("/show/<int:id>", methods=["GET"])
@login_required
@check_permission("view_empleado")
def show(id):
    
    """
    Muestra los detalles de un empleado específico, incluyendo su dirección, 
    contacto de emergencia y documentos como DNI, Título y CV.

    Args:
        id (int): ID del empleado a mostrar.

    Returns:
        str: Renderiza la plantilla HTML con la información del empleado, dirección, contacto de emergencia y documentos relevantes.

    """
    
    empleado = board.Empleado.get_empleado(id)  # Obtener empleado por ID
    documentos = Documento.get_documentos_empleado(id)  # Obtener documentos asociados al empleado
    dni = None  # Variable para almacenar el documento tipo DNI
    titulo = None  # Variable para almacenar el documento tipo Título
    cv = None  # Variable para almacenar el documento tipo CV

    # Itera sobre los documentos y asigna a las variables correspondientes
    for documento in documentos:
        if documento.document_type.value == 'DNI de Empleado':
            dni = documento  # Asigna el documento de tipo DNI
        elif documento.document_type.value == 'Título de Empleado':
            titulo = documento  # Asigna el documento de tipo Título
        elif documento.document_type.value == 'CV de Empleado':
            cv = documento  # Asigna el documento de tipo CV
            
   

    # Obtener dirección del empleado
    direccion = board.domicilio.query.get(empleado.domicilio)  # Obtener la dirección relacionada
    # Obtener contacto de emergencia del empleado
    contacto = board.contacto_emergencia.query.get(empleado.contacto_emergencia_id)  # Obtener el contacto de emergencia relacionado
    empleado.fecha_egreso = datetime.strptime(empleado.fecha_egreso, '%Y-%m-%d') if empleado.fecha_egreso else None 
    empleado.fecha_ingreso = datetime.strptime(empleado.fecha_ingreso, '%Y-%m-%d')  
    # Renderizar la plantilla con los datos del empleado, dirección, contacto y documentos
    return render_template(
        "empleado/show.html", 
        empleado=empleado, 
        direccion=direccion, 
        contacto=contacto, 
        dni=dni, 
        titulo=titulo, 
        cv=cv,
        
    )




# Delete empleado
@bp.route("/delete/<int:id>", methods=["POST"])
@login_required
@check_permission("delete_empleado")
def delete(id):
    """
    Elimina logicamente un empleado específico. Muestra un mensaje de éxito o error dependiendo del resultado de la operación.

    :param id: El ID del empleado a eliminar.
    :return: Redirección a la lista de empleados con un mensaje flash.
    """
    empleado = board.Empleado.get_empleado(id)
    
    if not empleado:
        flash("Empleado no encontrado", "error")
        return redirect(url_for("empleado.index"))

    board.Empleado.delete_empleado(id)
    flash("Empleado eliminado exitosamente", "success")
    return redirect(url_for("empleado.index"))

# Funcion auxiliar para verificar duplicados
def check_repetidos(dni, numero_afiliado, email, current_id=None):
    """
    Verifica si el DNI, el número de afiliado o el email ya existen en otro registro de empleado.

    :param dni: El DNI del empleado.
    :param numero_afiliado: El número de afiliado del empleado.
    :param email: El email del empleado.
    :param current_id: El ID del empleado actual (para evitar validar contra sí mismo en una actualización).
    :return: Un mensaje de error si hay duplicados, de lo contrario, None.
    """
    errores = []

    # Verificar duplicados de DNI
    empleado_dni = board.Empleado.get_empleado_by_dni(dni)
    if empleado_dni and (current_id is None or empleado_dni.id != current_id):
        errores.append("DNI repetido")
    
    # Verificar duplicados de email
    empleado_email = board.Empleado.get_empleado_by_email(email)
    if empleado_email and (current_id is None or empleado_email.id != current_id):
        errores.append("Email repetido")
    
    # Verificar duplicados de número de afiliado
    empleado_afiliado = board.Empleado.get_empleado_by_numero_afiliado(numero_afiliado)
    if empleado_afiliado and (current_id is None or empleado_afiliado.id != current_id):
        errores.append("Número de afiliado repetido")

    return ", ".join(errores) if errores else None


@bp.route("/empleado.restore<int:id>", methods=["POST"])
@login_required
@check_permission("edit_empleado")
def restore(id):
    """
    Restaura un empleado eliminado previamente. Muestra un mensaje de éxito o error dependiendo del resultado de la operación.

    :param id: El ID del empleado a restaurar.
    :return: Redirección a la lista de empleados con un mensaje flash.
    """
    empleado = board.Empleado.get_empleado(id)
    if not empleado:
        flash("Empleado no encontrado", "error")
        return redirect(url_for("empleado.index"))

    board.Empleado.restore_empleado(id)
    flash("Empleado restaurado exitosamente", "success")
    return redirect(url_for("empleado.index"))

# Funcion auxliar para obtener las profesiones
def get_profesiones():
    """
    Obtiene la lista de profesiones disponibles para los empleados.

    :return: Una lista de profesiones.
    """
    return ["Psicólogo/a", "Psicomotricista", "Médico/a", "Kinesiólogo/a", "Terapista Ocupacional", "Psicopedagogo/a", "Docente", "Profesor", "Fonoaudiólogo/a", "Veterinario/a", "Otro"]


