from flask import render_template, request, Blueprint, session
from src.web.handlers.auth import check_permission, login_required
from src.core.board.contenido import Contenido, Estado
from flask import flash, redirect, url_for
from src.web.handlers.auth import login_required, check_permission
from src.core.auth import User
from os import environ

bp = Blueprint('contenido', __name__, url_prefix='/contenido')

@bp.route('/', methods=['GET'])
@login_required
@check_permission('index_contenido')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = int(environ.get('PAGINATION_PER_PAGE', 25))
    titulo = request.args.get('titulo', '')
    autor = request.args.get('autor', '')
    estado = request.args.get('estado', '')
    ordenar_por = request.args.get('ordenar_por', 'created_at')
    orden = request.args.get('orden', 'asc')

    filters = {'titulo': titulo, 'autor': autor, 'estado': estado}
    contenidos = Contenido.list_contenido(page, per_page, filters, ordenar_por, orden)
    
    total_pages = contenidos.pages
    start = max(1, page - 2)
    end = min(total_pages, page + 2)
    
    return render_template('contenido/index.html', contenidos=contenidos, 
                           page=page, total_pages=total_pages, 
                           per_page=per_page, start=start, end=end, estados=Estado)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@check_permission('create_contenido')
def create():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        copete = request.form.get('copete')
        contenido = request.form.get('cuerpo')
        user_email = session.get('user')
        fecha_publicacion = None
        estado = Estado.borrador
        contenido = Contenido.create_contenido(titulo=titulo, copete=copete, contenido=contenido,user_email = user_email, fecha_publicacion=fecha_publicacion, estado=estado)
        flash('Contenido creado correctamente', 'success')
        return redirect(url_for('contenido.index'))
    
    return render_template('contenido/create.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@check_permission('edit_contenido')
def update(id):
    contenido = Contenido.get_contenido(Contenido,id)
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        copete = request.form.get('copete')
        contenido = request.form.get('cuerpo')
        autor = request.form.get('autor')
        contenido = Contenido.update_contenido(id, titulo=titulo, copete=copete, contenido=contenido, autor=autor)
        flash('Contenido actualizado correctamente', 'success')
        return redirect(url_for('contenido.index'))
    
    autores = User.get_all_users(User)
    return render_template('contenido/update.html', contenido=contenido, autores = autores)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@check_permission('delete_contenido')
def delete(id):
    contenido = Contenido.delete_contenido(id)
    flash('Contenido eliminado correctamente', 'success')
    return redirect(url_for('contenido.index'))

@bp.route('/show/<int:id>', methods=['GET'])
@login_required
@check_permission('view_contenido')
def show(id):
    contenido = Contenido.get_contenido(Contenido,id)
    return render_template('contenido/show.html', contenido=contenido)

@bp.route('/publicar/<int:id>', methods=['GET', 'POST'])
@login_required
@check_permission('edit_contenido')
def publicar(id):
    contenido = Contenido.get_contenido(Contenido,id)
    if contenido.estado == Estado.publicado:
        flash('El contenido ya se encuentra publicado', 'danger')
        return redirect(request.referrer or url_for('contenido.index'))
    
    contenido = Contenido.publicar_contenido(Contenido,id)
    flash('Contenido publicado correctamente', 'success')
    return redirect(request.referrer or url_for('contenido.index'))

@bp.route('/archivar/<int:id>', methods=['GET', 'POST'])
@login_required
@check_permission('edit_contenido')
def archivar(id):
    contenido = Contenido.get_contenido(Contenido,id)
    if contenido.estado == Estado.archivado:
        flash('El contenido ya se encuentra archivado', 'danger')
        return redirect(request.referrer or url_for('contenido.index'))
    
    contenido = Contenido.archivar_contenido(Contenido,id)
    flash('Contenido archivado correctamente', 'success')
    return redirect(request.referrer or url_for('contenido.index'))
        