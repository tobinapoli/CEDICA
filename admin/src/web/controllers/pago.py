from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.web.handlers.auth import login_required
from src.core.database import db
from src.core.board import Pago
from datetime import datetime
from src.web.handlers.auth import check_permission
from src.core.board import Empleado
from os import environ
# Crear un blueprint para las rutas de pagos
bp = Blueprint("pago", __name__, url_prefix="/pagos")


@bp.route("/", methods=["GET"])
@login_required
@check_permission("index_pago")
def index():
    """
    Muestra el listado de pagos con opciones de paginación, filtrado, 
    y ordenación por fecha, beneficiario y tipo de pago.

    Returns:
        str: Renderiza la plantilla del listado de pagos con filtros aplicados.
    """
    # Parámetros de filtro obtenidos de los argumentos de la URL
    filters = {
        'beneficiario': request.args.get('beneficiario', '').strip(),
        'tipo_de_pago': request.args.get('tipo_de_pago', '').strip(),
        'fecha_inicio': request.args.get('fecha_inicio', '').strip(),
        'fecha_fin': request.args.get('fecha_fin', '').strip()
    }

    # Parámetros de ordenación
    order_by = request.args.get('ordenar_por', 'fecha')
    order_direction = request.args.get('orden', 'asc')

    # Configuración de la paginación
    page = request.args.get('page', 1, type=int)
    per_page = int(environ.get('PAGINATION_PER_PAGE', 25))

    # Obtener los pagos filtrados y ordenados
    pagos_paginated = Pago.list_pagos(
        filters=filters,
        order_by=order_by,
        order_direction=order_direction,
        page=page,
        per_page=per_page
    )

    # Datos adicionales para la vista
    tipos_de_pago = Pago.get_tipos_de_pago()
    total_pages = pagos_paginated.pages
    start = max(1, page - 2)
    end = min(total_pages, page + 2)
    current_date = datetime.now().strftime('%d/%m/%Y')

    # Renderizar plantilla
    return render_template(
        "pago/index.html",
        form_data=request.form,
        pagos=pagos_paginated.items,
        pagination=pagos_paginated,
        filters=filters,
        order_by=order_by,
        order_direction=order_direction,
        tipos_de_pago=tipos_de_pago,
        page=page,
        total_pages=total_pages,
        start=start,
        end=end,
        current_date=current_date
    )



@bp.route("/show/<int:id>", methods=["GET"])
@login_required
@check_permission("show_pago")
def show(id):
    """
    Muestra un pago específico con todos sus datos.

    Args:
        id (int): ID del pago a mostrar.

    Returns:
        str: Renderiza la plantilla con los detalles del pago o redirige
        al índice con un mensaje de error si el pago no existe.
    """
    pago = Pago.get_pago(id)
    if not pago:
        flash("El pago no existe.", "error")
        return redirect(url_for("pago.index"))

    return render_template("pago/show.html", pago=pago)



@bp.route('/create', methods=['GET', 'POST'])
@login_required
@check_permission("create_pago")
def create():
    """
    Crea un nuevo pago indicando los valores de los atributos necesarios.

    Returns:
        str: Renderiza la plantilla de creación de pago. Redirige al índice
        si el pago se crea exitosamente o muestra errores si la creación falla.
    """
    current_date = datetime.now().strftime('%Y-%m-%d')
    if request.method == "POST":
        beneficiario_id = request.form.get("beneficiario")  
        monto = request.form.get("monto")
        fecha = request.form.get("fecha")
        tipo_de_pago = request.form.get("tipo_de_pago")
        descripcion = request.form.get("descripcion")

        error = check_repetidos(fecha, beneficiario_id, tipo_de_pago, monto)
        if error:
            flash(error, "error")
            tipos_de_pago = Pago.get_tipos_de_pago()
            empleados = Empleado.get_all_empleado()
            return render_template("pago/create.html", form_data=request.form, tipos_de_pago=tipos_de_pago, empleados=empleados, current_date = current_date)

        try:
            monto_float = float(monto)
            if monto_float <= 0:
                raise ValueError("El monto no puede ser negativo.")
        except ValueError: 
            flash("Monto inválido. Asegúrate de ingresar un número válido.", "error")
            tipos_de_pago = Pago.get_tipos_de_pago()
            empleados = Empleado.get_all_empleado()
            return render_template("pago/create.html", form_data=request.form, tipos_de_pago=tipos_de_pago, empleados=empleados, current_date = current_date)

        Pago.create_pago(
            beneficiario_id=beneficiario_id if tipo_de_pago == "Honorarios" else None,
            monto=monto_float,
            fecha=fecha,
            tipo_de_pago=tipo_de_pago,
            descripcion=descripcion
        )
        flash("Pago registrado exitosamente", "success")
        return redirect(url_for("pago.index"))

    tipos_de_pago = Pago.get_tipos_de_pago()
    empleados = Empleado.get_all_empleado()
    return render_template("pago/create.html", form_data={}, tipos_de_pago=tipos_de_pago, empleados=empleados)





@bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
@check_permission("edit_pago")
def update(id):
    """
    Actualiza un pago existente.

    Args:
        id (int): ID del pago a actualizar.

    Returns:
        str: Renderiza la plantilla de actualización de pago. Redirige al índice
        si el pago no existe o si la actualización se realiza correctamente,
        o muestra errores si la actualización falla.
    """
    pago = Pago.get_pago(id)
    if not pago:
        return redirect(url_for("pago.index"))

    if request.method == "POST":
        beneficiario_id = request.form.get("beneficiario")
        monto = request.form["monto"]
        fecha = request.form["fecha"]
        tipo_de_pago = request.form["tipo_de_pago"]
        descripcion = request.form["descripcion"]

        error = check_repetidos(fecha, beneficiario_id, tipo_de_pago,monto, current_id=id)
        if error:
            flash(error, "error")
            tipos_de_pago = Pago.get_tipos_de_pago()
            empleados = Empleado.get_all_empleado()
            return render_template("pago/update.html", pago=pago, tipos_de_pago=tipos_de_pago,empleados=empleados, form_data=request.form)
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                raise ValueError("El monto no puede ser negativo.")
        except ValueError: 
            flash("Monto inválido. Asegúrate de ingresar un número válido.", "error")
            tipos_de_pago = Pago.get_tipos_de_pago()
            empleados = Empleado.get_all_empleado()
            return render_template("pago/update.html", pago=pago, tipos_de_pago=tipos_de_pago, empleados=empleados, form_data=request.form)

        Pago.update_pago(id, beneficiario_id=beneficiario_id if tipo_de_pago == "Honorarios" else None, monto=monto, fecha=fecha, tipo_de_pago=tipo_de_pago, descripcion=descripcion)
        flash("Pago actualizado exitosamente", "success")
        return redirect(url_for("pago.index"))

    empleados = Empleado.get_all_empleado()
    tipos_de_pago = Pago.get_tipos_de_pago()
    return render_template("pago/update.html", pago=pago, tipos_de_pago=tipos_de_pago, empleados = empleados, form_data={})


@bp.route("/delete/<int:id>", methods=["POST"])
@login_required
@check_permission("delete_pago")
def delete(id):
    """
    Elimina un pago existente.

    Args:
        id (int): ID del pago a eliminar.

    Returns:
        str: Redirige al índice con un mensaje de éxito tras la eliminación.
    """
    Pago.delete_pago(id)
    flash("Pago eliminado exitosamente", "success")
    return redirect(url_for("pago.index"))


def check_repetidos(fecha, beneficiario_id, tipo_de_pago, monto,current_id=None):
    """
    Verifica que el pago a crear o actualizar no sea uno existente
    para evitar duplicados.

    Args:
        fecha (str): Fecha del pago.
        beneficiario_id (int): ID del beneficiario.
        tipo_de_pago (str): Tipo de pago.
        monto (float): Monto del pago.
        current_id (int, optional): ID del pago actual para evitar
        verificar contra sí mismo.

    Returns:
        str: Mensaje de error si hay un pago duplicado; None si no hay duplicados.
    """
    errores = []

    pago_existente = Pago.get_pago_by_fecha_beneficiario(fecha, beneficiario_id, tipo_de_pago,monto)
    if pago_existente and (current_id is None or pago_existente.id != current_id):
        errores.append("Ya existe un pago para este beneficiario en esta fecha con el mismo tipo de pago y monto")

    if errores:
        return '. '.join(errores)

    return None
