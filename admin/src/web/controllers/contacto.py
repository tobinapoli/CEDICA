from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.board.consulta import Consulta
from src.web.handlers.auth import login_required
from os import environ
from src.web.handlers.auth import check_permission
bp = Blueprint('contactos', __name__, url_prefix='/contactos')

@bp.route('/', methods=['GET'])
@login_required
@check_permission("index_consulta")
def index():
    """Listado de consultas con paginación, filtros y ordenación."""
    page = request.args.get('page', 1, type=int)
    per_page = int(environ.get('PAGINATION_PER_PAGE', 25))
    estado = request.args.get('estado')
    orden = request.args.get('orden', 'asc')  # Por defecto, orden ascendente

    # Filtrar por estado
    filters = {"estado": estado} if estado else {}

    # Obtener consultas paginadas con filtros y ordenación
    consultas_paginated = Consulta.list_consultas(
        page=page,
        per_page=per_page,
        filters=filters,
        sort_by='created_at',
        order=orden
    )
    total_pages = consultas_paginated.pages
    start = max(1, page - 2)
    end = min(total_pages, page + 2)

    return render_template(
        'contactos/index.html',
        consultas=consultas_paginated.items,
        pagination=consultas_paginated,
        estado_filtro=estado,
        orden=orden,total_pages=total_pages,start=start, end=end,page=page
    )



@bp.route('/create', methods=['GET', 'POST'])
@login_required
@check_permission("create_consulta")
def create():
    """Crear una nueva consulta (solo si es necesario desde el admin)."""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        mensaje = request.form.get('mensaje')

        try:
            Consulta.create(nombre=nombre, correo=correo, mensaje=mensaje, estado="created")
            flash('Consulta creada correctamente.', 'success')
            return redirect(url_for('contactos.index'))
        except Exception as e:
            flash(f"Error al crear la consulta: {str(e)}", 'danger')

    return render_template('contactos/create.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@check_permission("edit_consulta")
def update(id):
    """Actualizar estado o comentario de una consulta."""
    consulta = Consulta.get_consulta(id)
    if not consulta:
        flash('Consulta no encontrada.', 'danger')
        return redirect(url_for('contactos.index'))

    if request.method == 'POST':
        estado = request.form.get('estado')
        comentario_interno = request.form.get('comentario')
        try:
            Consulta.update_consulta(id, estado=estado, comentario_interno=comentario_interno)
            flash('Consulta actualizada correctamente.', 'success')
            return redirect(url_for('contactos.show', id=id))
        except Exception as e:
            flash(f"Error al actualizar la consulta: {str(e)}", 'danger')

    return render_template('contactos/update.html', consulta=consulta)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@check_permission("delete_consulta")
def delete(id):
    """Eliminar una consulta."""
    try:
        Consulta.delete_consulta(id)
        flash('Consulta eliminada correctamente.', 'success')
    except Exception as e:
        flash(f"Error al eliminar la consulta: {str(e)}", 'danger')

    return redirect(url_for('contactos.index'))

@bp.route('/show/<int:id>', methods=['GET'])
@login_required
@check_permission("show_consulta")
def show(id):
    """Mostrar el detalle de una consulta específica."""
    consulta = Consulta.get_consulta(id)
    if not consulta:
        flash('Consulta no encontrada.', 'danger')
        return redirect(url_for('contactos.index'))
    
    return render_template('contactos/show.html', consulta=consulta)
