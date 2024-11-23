from flask import send_file
from flask import Blueprint
from src.core.board.documento import Documento
from src.core.board.documento import TipoDocumento, TipoTitular
from flask import current_app, flash, redirect, url_for, request, render_template
import io
import ulid
from os import fstat

bp = Blueprint('documentos', __name__, url_prefix='/documentos')

@bp.route('/create', methods=['POST'])
def create(file, document_type,titular_id,tipo_titular, tipo_entrada,link=None,):
    """
    Crea un nuevo documento, ya sea subiendo un archivo o usando un enlace.

    Args:
        file (FileStorage): El archivo a subir.
        document_type (TipoDocumento): Tipo de documento a crear.
        titular_id (int): ID del titular del documento.
        tipo_titular (TipoTitular): Tipo de titular (ejemplar, empleado, jinete).
        tipo_entrada (str): Tipo de entrada, puede ser "link" o "archivo".
        link (str, optional): Enlace al documento si el tipo de entrada es "link".

    Returns:
        None
    """
    if tipo_entrada == "link":
        Documento.create_document(
            Documento,
            filename=link, 
            document_type=document_type, 
            file_url=link, 
            titular_id=titular_id,
            tipo_titular=tipo_titular, 
            is_link = True)
    else:
        nombre = ulid.ulid()
        client = current_app.storage.client
        size = fstat(file.fileno()).st_size
                
        client.put_object(
            "grupo46",
            f"{nombre}-{file.filename}",
            file,
            size,
            content_type=file.content_type,
        )
        Documento.create_document(
            Documento,
            filename=file.filename, 
            document_type=document_type, 
            file_url=f"{nombre}-{file.filename}", 
            titular_id=titular_id,
            tipo_titular=tipo_titular,
            is_link = False)
    
    
   

@bp.route('/download/<int:document_id>', methods=["GET"])
def download(document_id):
    """
    Descarga un documento dado su ID.

    Args:
        document_id (int): ID del documento a descargar.

    Returns:
        Response: Flujo de bytes del archivo para descargar, o un mensaje de error.
    """
    documento = Documento.query.get(document_id)
    if documento:
        client = current_app.storage.client
        file_path = f"{documento.file_url}"
        
        # Obtiene el objeto del archivo como un flujo de bytes
        file_obj = client.get_object("grupo46", file_path)
        
        # Se necesita crear un buffer de bytes para enviar el archivo
        return send_file(io.BytesIO(file_obj.read()),  # Leer el contenido del objeto
                         download_name=documento.filename,  # Nombre del archivo para la descarga
                         as_attachment=True,  # Descargar como archivo adjunto
                         mimetype=documento.get_mime_type())  # Usar el método para obtener el tipo MIME
    else:
        return "Documento no encontrado", 404




@bp.route('/show/<int:document_id>', methods=["GET"])
def show(document_id):
    """
    Muestra un documento dado su ID.

    Args:
        document_id (int): ID del documento a mostrar.

    Returns:
        Response: Flujo de bytes del archivo para mostrar, o un mensaje de error.
    """
    documento = Documento.query.get(document_id)
    if documento:
        client = current_app.storage.client
        file_path = f"{documento.file_url}"
        
        # Obtiene el objeto del archivo como un flujo de bytes
        file_obj = client.get_object("grupo46", file_path)
        
        # Usa send_file para enviar el archivo al cliente
        return send_file(io.BytesIO(file_obj.read()),
                         download_name=documento.filename,  
                         as_attachment=False, 
                         mimetype=documento.get_mime_type())  # Usar el método para obtener el tipo MIME
    else:
        return "Documento no encontrado", 404
    
@bp.route('/delete/<int:document_id>', methods=["GET"])
def delete(document_id):
    """
    Elimina un documento dado su ID.

    Args:
        document_id (int): ID del documento a eliminar.

    Returns:
        Response: Redirección después de eliminar el documento.
    """
    documento = Documento.query.get(document_id)
    if not documento:
        flash("Documento no encontrado", "danger")
        return redirect(url_for('ejemplares.index'))  # Redirigir a la lista si no se encuentra el documento

    if documento.is_link:
        Documento.delete(documento)
        flash("Documento eliminado", "success")
    else:
        client = current_app.storage.client
        file_path = f"{documento.file_url}"
        client.remove_object("grupo46", file_path)
        Documento.delete(documento)
        flash("Documento eliminado", "success")
    
    return redirect(url_for('ejemplares.show', id=documento.ejemplar_id) + '#section-docs')  # Redirigir al show del ejemplar correspondiente

@bp.route('/create_doc_ejemplar/<int:ejemplar_id>', methods=['GET', 'POST'])
def create_doc_ejemplar(ejemplar_id):
    """
    Crea documentos para un ejemplar dado su ID.

    Args:
        ejemplar_id (int): ID del ejemplar para el cual se crearán los documentos.

    Returns:
        Response: Redirección después de crear los documentos o el formulario de creación.
    """
    if request.method == 'POST':
        tipos_documento = request.form.getlist('tipo_documento[]')
        archivos = request.files.getlist('documentos[]')
        tipos_entrada = request.form.getlist('documento_tipo[]')
        enlaces = request.form.getlist('links[]')

        for i in range(len(tipos_documento)):
            tipo_doc = tipos_documento[i]
            
            archivo = create(
                file=archivos[i],
                link=enlaces[i], 
                document_type=tipo_doc, 
                titular_id=ejemplar_id,
                tipo_titular = TipoTitular.ejemplar, 
                tipo_entrada= tipos_entrada[i]
            )

        flash('Documento creado correctamente', 'success')
        return redirect(url_for('ejemplares.show', id=ejemplar_id))

    tipos_docs = TipoDocumento.get_tipo_doc_ejemplar()
    return render_template('documento/create.html', ejemplar_id=ejemplar_id, tipos_docs=tipos_docs)

@bp.route('/create_doc_empleado/<int:empleado_id>/<tipo_doc>', methods=['POST'])
def create_doc_empleado(empleado_id, tipo_doc):
    """
    Crea un documento para un empleado dado su ID.

    Args:
        empleado_id (int): ID del empleado para el cual se creará el documento.
        tipo_doc (str): Tipo de documento a crear.

    Returns:
        Response: Redirección después de crear el documento.
    """
    if request.method == 'POST':
        archivo = request.files.get('documento')
        create(
            file=archivo,
            document_type=tipo_doc, 
            titular_id=empleado_id,
            tipo_titular=TipoTitular.empleado,
            tipo_entrada="archivo"
        )
        flash('Documento creado correctamente', 'success')
        return redirect(url_for('empleado.show', id=empleado_id))
        
@bp.route('/delete_doc_empleado/<int:document_id>', methods=["GET"])
def delete_doc_empleado(document_id): 
    """
    Elimina un documento de un empleado dado su ID.

    Args:
        document_id (int): ID del documento a eliminar.

    Returns:
        Response: Redirección después de eliminar el documento.
    """  
    documento = Documento.query.get(document_id)
    if not documento:
        flash("Documento no encontrado", "danger")
        return redirect(url_for('empleado.show', id=documento.empleado.id))  # Redirigir a la lista si no se encuentra el documento

    
    client = current_app.storage.client
    file_path = f"{documento.file_url}"
    client.remove_object("grupo46", file_path)
    Documento.delete(documento)
    flash("Documento eliminado", "success")

    return redirect(url_for('empleado.show', id=documento.empleado.id))  # Redirigir al show del ejemplar correspondiente



@bp.route('/create_doc_jinete_amazona/<int:jinete_id>/', methods=['GET', 'POST'])
def create_doc_jinete(jinete_id):
    """
    Crea documentos para un jinete dado su ID.

    Args:
        jinete_id (int): ID del jinete para el cual se crearán los documentos.

    Returns:
        Response: Redirección después de crear los documentos o el formulario de creación.
    """    
    if request.method == 'POST':
        tipos_documento = request.form.getlist('tipo_documento[]')
        archivos = request.files.getlist('documentos[]')
        tipos_entrada = request.form.getlist('documento_tipo[]')
        enlaces = request.form.getlist('links[]')
            
        for i in range(len(tipos_documento)):
            tipo_doc = tipos_documento[i]
            create(
                file=archivos[i],
                link=enlaces[i], 
                document_type=tipo_doc, 
                titular_id=jinete_id,
                tipo_titular = TipoTitular.jya, 
                tipo_entrada= tipos_entrada[i]
            )
        flash('Documento creado correctamente', 'success')
        return redirect(url_for('jinete_amazona.show', id=jinete_id))

    tipos_docs = TipoDocumento.get_tipo_doc_jinetes()
    return render_template('documento/create_jinete.html', id=jinete_id, tipos_docs=tipos_docs)
    
    
        
@bp.route('/delete_jinete/<int:document_id>', methods=["GET"])
def delete_jinete(document_id):
    """
    Elimina un documento asociado a un jinete dado su ID.

    Args:
        document_id (int): ID del documento a eliminar.

    Returns:
        Response: Redirección a la vista de índice de jinetes si el documento no se encuentra, 
                  o a la vista de un jinete específico después de la eliminación.
    """
    documento = Documento.query.get(document_id)
    if not documento:
        flash("Documento no encontrado", "danger")
        return redirect(url_for('jinete_amazona.index'))  # Redirigir a la lista si no se encuentra el documento

    if documento.is_link:
        Documento.delete(documento)
        flash("Documento eliminado", "success")
    else:
        client = current_app.storage.client
        file_path = f"{documento.file_url}"
        client.remove_object("grupo46", file_path)
        Documento.delete(documento)
        flash("Documento eliminado", "success")
    
    return redirect(url_for('jinete_amazona.show', id=documento.jinete_amazona.id) + '#section-docs')  # Redirigir al show del ejemplar correspondiente