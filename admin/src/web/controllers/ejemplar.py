from flask import render_template, request, Blueprint
from src.web.handlers.auth import check_permission, login_required
from src.core import board
from flask import flash, redirect, url_for, jsonify
from src.web.handlers.auth import login_required, check_permission
from src.core.board.documento import Documento
from src.web.controllers import documento as documento_controller
from src.core.board.documento import TipoDocumento, TipoTitular
from werkzeug.utils import secure_filename
from os import environ
from src.web import storage
from os import fstat
from flask import current_app
import ulid

bp = Blueprint('ejemplares', __name__, url_prefix='/ejemplares')

@bp.route('/', methods=['GET'])
@login_required
@check_permission('index_ejemplares')
def index():
    """
    Renderiza la lista de ejemplares con filtros y opciones de ordenamiento.

    Los filtros y opciones de ordenamiento se obtienen de los parámetros de la consulta 
    en la URL. Se cargan los ejemplares y documentos asociados, y se devuelve la plantilla 
    de la vista de índice de ejemplares.

    Returns:
        str: Renderiza la plantilla 'ejemplares/index.html' con los datos de ejemplares, 
        tipos de jinete y documentos.
    """
    section = request.args.get('section', 'ejemplares')
    ejemplares_page = request.args.get('page', 1, type=int)
    documentos_page = request.args.get('page2', 1, type=int)
    
    
    per_page = int(environ.get('PAGINATION_PER_PAGE', 25))
    

   

    docs_filters = {
        'titulo': request.args.get('titulo', ''),
        'tipo_documento': request.args.get('tipo_documento', '')
    }

    filters = {
        'nombre': request.args.get('nombre', ''),
        'tipo_de_jinete': request.args.get('tipo_de_jinete', ''),
    }

    order_by = request.args.get('order_by', 'nombre')
    order_direction = request.args.get('order_direction', 'asc')

    order_by2 = request.args.get('order_by2', 'fecha_subida')
    order_direction2 = request.args.get('order_direction2', 'asc')
    
    ejemplares, total, current_page, total_pages = board.ejemplar.list_ejemplar(filters=filters, order_by=order_by, order_direction=order_direction, page=ejemplares_page, per_page=per_page)

    tipos_de_jinete = board.tipo_de_jinete.list_tipo_de_jinete()
    documentos, total2, current_page2, total_pages2 = Documento.get_filtered_documentos(docs_filters, order_by2, order_direction2, page=documentos_page, per_page=per_page, tipo_titular=TipoTitular.ejemplar)
    
    documentos_con_ejemplares = []
    for documento in documentos:
        ejemplar = None
        if documento.tipo_titular == TipoTitular.ejemplar:
            if documento.ejemplar_id:
                ejemplar = board.ejemplar.get_ejemplar(documento.ejemplar_id)
                documentos_con_ejemplares.append({
                    'documento': documento,
                    'ejemplar': ejemplar
                })

    start = max(1, ejemplares_page - 2)
    end = min(total_pages, ejemplares_page + 2)
    
    start2 = max(1, documentos_page - 2)
    end2 = min(total_pages2, documentos_page + 2)
    
    tipos_docs = TipoDocumento.get_tipo_doc_ejemplar()
    return render_template('ejemplares/index.html', ejemplares=ejemplares, 
                           total=total, current_page=current_page, 
                           total_pages=total_pages,
                           tipos_de_jinete=tipos_de_jinete, documentos=documentos_con_ejemplares, 
                           section=section, tipos_docs=tipos_docs,
                           total2=total2, current_page2=current_page2, 
                           total_pages2=total_pages2, start=start, end=end, start2=start2, end2=end2)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@check_permission('create_ejemplares')
def create():
    """
    Crea un nuevo ejemplar a partir de los datos proporcionados en un formulario.

    Si el método de la solicitud es POST, se procesan los datos del formulario, se crea el 
    ejemplar y se asocian los documentos. Si es GET, se renderiza el formulario para 
    crear un nuevo ejemplar.

    Returns:
        str: Renderiza la plantilla 'ejemplares/create.html' si el método es GET; 
        de lo contrario, redirige a la lista de ejemplares después de la creación exitosa.
    """
    if request.method == 'POST':
        # Convierte el string en una lista de enteros
        tipos_documento = request.form.getlist('tipo_documento[]')
        tipos_entrada = request.form.getlist('documento_tipo[]')
        archivos = request.files.getlist('documentos[]')
        enlaces = request.form.getlist('links[]')

        entrenadores_ids = request.form.get('entrenadores')
        if not entrenadores_ids:
            entrenadores_objects = [] 
        else:
            entrenadores_ids = [int(id) for id in entrenadores_ids.split(',')]
            entrenadores_objects = board.Empleado.query.filter(board.Empleado.id.in_(entrenadores_ids)).all()

        client = current_app.storage.client

        ejemplar = board.ejemplar.create_ejemplar(
            nombre=request.form['nombre'],
            fecha_nacimiento=request.form['fecha_nacimiento'],
            genero=request.form['genero'],
            raza=request.form['raza'],
            pela=request.form['pela'],
            tipo_de_adquisicion=request.form['tipo_de_adquisicion'].lower(),
            fecha_ingreso=request.form['fecha_ingreso'],
            sede=request.form['sede'],
            entrenadores=entrenadores_objects,
            tipo_jinete=request.form['tipo_jinete']
        )
        if not tipos_documento == ['']:
            for i in range(len(tipos_documento)):
                tipo_doc = tipos_documento[i]
                tipo_entrada = tipos_entrada[i]  
                archivo = documento_controller.create(
                    file=archivos[i],
                    link=enlaces[i], 
                    document_type=tipo_doc, 
                    titular_id=ejemplar.id,
                    tipo_titular=TipoTitular.ejemplar, 
                    tipo_entrada=tipo_entrada
                )

        flash('Ejemplar creado correctamente', 'success')
        return redirect(url_for('ejemplares.index'))

    empleados = [empleado.to_dict() for empleado in board.Empleado.list_empleado()]
    tipos_docs = TipoDocumento.get_tipo_doc_ejemplar()
    return render_template('ejemplares/create.html', empleados=empleados, tipos_de_jinete=board.tipo_de_jinete.list_tipo_de_jinete(), tipos_docs=tipos_docs)


@bp.route("/show/<int:id>", methods=["GET"])
@login_required
@check_permission("view_ejemplares")
def show(id):
    """
    Muestra los detalles de un ejemplar específico.

    Obtiene el ejemplar y sus documentos asociados a partir del ID proporcionado 
    en la URL y renderiza la plantilla correspondiente.

    Args:
        id (int): ID del ejemplar a mostrar.

    Returns:
        str: Renderiza la plantilla 'ejemplares/show.html' con los datos del ejemplar 
        y sus documentos.
    """
    ejemplar = board.ejemplar.get_ejemplar(id)
    documentos = ejemplar.documentos
    return render_template('ejemplares/show.html', ejemplar=ejemplar, documentos=documentos)


@bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
@check_permission("update_ejemplares")
def update(id):
    """
    Actualiza los datos de un ejemplar específico.

    Si el método de la solicitud es POST, se procesan los datos del formulario 
    y se actualiza el ejemplar correspondiente. Si es GET, se renderiza el formulario 
    con los datos actuales del ejemplar.

    Args:
        id (int): ID del ejemplar a actualizar.

    Returns:
        str: Renderiza la plantilla 'ejemplares/update.html' si el método es GET; 
        de lo contrario, redirige a la vista de detalles del ejemplar después de la 
        actualización exitosa.
    """
    ejemplar = board.ejemplar.get_ejemplar(id)
    if request.method == 'POST':
        
        entrenadores_ids = request.form.get('entrenadores')
        if not entrenadores_ids:
            entrenadores_objects = []
        else:
            entrenadores_ids = [int(id) for id in entrenadores_ids.split(',')]
            entrenadores_objects = board.Empleado.query.filter(board.Empleado.id.in_(entrenadores_ids)).all()

        board.ejemplar.update_ejemplar(
            id,
            nombre=request.form['nombre'],
            fecha_nacimiento=request.form['fecha_nacimiento'],
            genero=request.form['genero'],
            raza=request.form['raza'],
            pela=request.form['pela'],
            tipo_de_adquisicion=request.form['tipo_de_adquisicion'].lower(),
            fecha_ingreso=request.form['fecha_ingreso'],
            sede=request.form['sede'],
            entrenadores=entrenadores_objects,
            tipo_jinete=request.form['tipo_jinete']
        )

        flash('Ejemplar actualizado correctamente', 'success')
        return redirect(url_for('ejemplares.show', id=id))

    empleados = [empleado.to_dict() for empleado in board.Empleado.list_empleado()]
    entrenadores_ejemplar_ids = [empleado.to_dict()['id'] for empleado in ejemplar.entrenadores]
    tipos_docs = TipoDocumento.get_tipo_doc_ejemplar()
    tipos_de_jinete = board.tipo_de_jinete.list_tipo_de_jinete()
    return render_template('ejemplares/update.html', ejemplar=ejemplar, empleados=empleados, tipos_de_jinete=tipos_de_jinete, entrenadores_ejemplar=entrenadores_ejemplar_ids, tipos_docs=tipos_docs)


@bp.route("/delete/<int:id>", methods=["POST"])
@login_required
@check_permission("delete_ejemplares")
def delete(id):
    """
    Elimina un ejemplar específico.

    Elimina el ejemplar correspondiente al ID proporcionado y redirige a la 
    lista de ejemplares, mostrando un mensaje de éxito.

    Args:
        id (int): ID del ejemplar a eliminar.

    Returns:
        str: Redirige a la vista de índice de ejemplares.
    """
    board.ejemplar.delete_ejemplar(id)
    flash('Ejemplar eliminado correctamente', 'success')
    return redirect(url_for('ejemplares.index'))
