from enum import Enum as PyEnum
from datetime import datetime
import mimetypes
from src.core.database import db

class TipoDocumento(PyEnum):
    """
    Enumeración de tipos de documentos que pueden ser asociados a ejemplares,
    empleados y jinetes.
    """
    # Docs de ejemplares
    ficha_general = "Ficha general del caballo"
    planificacion_entrenamiento = "Planificación de Entrenamiento"
    informe_evolucion = "Informe de Evolución"
    carga_imagenes = "Carga de Imágenes"
    registro_veterinario = "Registro veterinario"
    # Docs de empleados
    dni_empleado = "DNI de Empleado"  # Ejemplo para otros módulos
    titulo_empleado = "Título de Empleado" 
    cv_empleado = "CV de Empleado" 
    # Docs Jinetes
    entrevista = "Entrevista"
    evaluación = "Evaluacion"
    planificaciones = "Planificaciones"
    evolución = "Evolucion"
    crónicas = "Cronicas"
    documental = "Documental"
    
    def get_tipo_doc_empleado():
        """
        Devuelve una lista de tipos de documentos para empleados.

        Returns:
            list: Lista de tipos de documentos relacionados con empleados.
        """
        return [TipoDocumento.dni_empleado, TipoDocumento.titulo_empleado, TipoDocumento.cv_empleado]
    def get_tipo_doc_ejemplar():
        """
        Devuelve una lista de tipos de documentos para ejemplares.

        Returns:
            list: Lista de tipos de documentos relacionados con ejemplares.
        """
        return [TipoDocumento.ficha_general, TipoDocumento.planificacion_entrenamiento, TipoDocumento.informe_evolucion, TipoDocumento.carga_imagenes, TipoDocumento.registro_veterinario]
    def get_tipo_doc_jinetes():
        """
        Devuelve una lista de tipos de documentos para jinetes.

        Returns:
            list: Lista de tipos de documentos relacionados con jinetes.
        """
        return [TipoDocumento.entrevista, TipoDocumento.evaluación, TipoDocumento.planificaciones, TipoDocumento.evolución, TipoDocumento.crónicas, TipoDocumento.documental]
    

    
class TipoTitular(PyEnum):
    """
    Enumeración de tipos de titulares que pueden tener documentos.
    """
    empleado = "Empleado"
    ejemplar = "Ejemplar"
    jya = "Jinete y Amazona"
    
class Documento(db.Model):
    """
    Modelo de base de datos para representar un documento asociado a un 
    empleado, ejemplar o jinete.
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(512), nullable=False)
    document_type = db.Column(db.Enum(TipoDocumento), nullable=False)
    tipo_titular = db.Column(db.Enum(TipoTitular), nullable=False)
    ejemplar_id = db.Column(db.Integer, db.ForeignKey('ejemplar.id'), nullable=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=True)  
    jinete_id = db.Column(db.Integer, db.ForeignKey('jinete_amazona.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_link = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """
        Devuelve una representación en cadena del documento.

        Returns:
            str: Representación del documento, incluyendo su nombre de archivo.
        """
        return f'<Document {self.filename}>'
    
    def create_document(cls,**kwargs):
        """
        Crea un nuevo documento y lo guarda en la base de datos.

        Args:
            kwargs (dict): Parámetros del documento a crear, que incluyen
                           'filename', 'document_type', 'file_url',
                           'tipo_titular', 'is_link' y 'titular_id'.

        Returns:
            Documento: El documento creado.
        """
        document = cls(
        filename=kwargs["filename"],
        document_type=kwargs["document_type"],
        file_url=kwargs["file_url"],
        tipo_titular=kwargs["tipo_titular"],
        is_link=kwargs["is_link"]
    )

        # Asigna el titular_id dependiendo del tipo de titular
        if kwargs["tipo_titular"] == TipoTitular.empleado:
            document.empleado_id = kwargs["titular_id"]
        elif kwargs["tipo_titular"] == TipoTitular.ejemplar:
            document.ejemplar_id = kwargs["titular_id"]
        else:
            document.jinete_id = kwargs["titular_id"]
        
        
        db.session.add(document)
        db.session.commit()
        return document
    
    def get_documentos_ejemplar(cls,ejemplar_id):
        """
        Obtiene todos los documentos asociados a un ejemplar.

        Args:
            ejemplar_id (int): Identificador del ejemplar.

        Returns:
            list: Lista de documentos asociados al ejemplar.
        """
        return cls.query.filter_by(ejemplar_id=ejemplar_id).all()
    
    def get_mime_type(self):
        """
        Obtiene el tipo MIME del archivo del documento.

        Returns:
            str: Tipo MIME del archivo o 'application/octet-stream' si no se puede determinar.
        """
        # Obtiene la extensión del archivo
        ext = self.filename.rsplit('.', 1)[-1].lower()  # Obtener la extensión del nombre del archivo
        mime_type, _ = mimetypes.guess_type(f'file.{ext}')  # Usa mimetypes para inferir el tipo MIME
        return mime_type or 'application/octet-stream'  # Devuelve un tipo por defecto si no se encuentra
    
    def delete(self):
        """
        Elimina el documento de la base de datos.
        """
        db.session.delete(self)
        db.session.commit()
        
    def get_documentos():
        """
        Obtiene todos los documentos de la base de datos.

        Returns:
            list: Lista de todos los documentos.
        """
        return Documento.query.all()
    
    @staticmethod
    def get_filtered_documentos(filters, order_by, order_direction, page, per_page, tipo_titular=None):
        """
        Obtiene una lista filtrada y paginada de documentos.

        Args:
            filters (dict): Diccionario de filtros aplicados a los documentos.
            order_by (str): Campo por el cual ordenar (ejemplo: 'titulo', 'fecha_subida').
            order_direction (str): Dirección de la ordenación ('asc' para ascendente, 'desc' para descendente).
            page (int): Página actual de la paginación.
            per_page (int): Número de documentos por página.

        Returns:
            tuple: Elementos filtrados, total de resultados, página actual, y número total de páginas.
        """
        query = Documento.query
        
        if tipo_titular:
            query = query.filter(Documento.tipo_titular == tipo_titular)

        if filters['titulo']:
            query = query.filter(Documento.filename.ilike(f"%{filters['titulo']}%"))
        
        if filters['tipo_documento']:
            query = query.filter(Documento.document_type == filters['tipo_documento'])

        if order_by == 'titulo':
            query = query.order_by(Documento.filename.asc() if order_direction == 'asc' else Documento.filename.desc())
        elif order_by == 'fecha_subida':
            query = query.order_by(Documento.created_at.asc() if order_direction == 'asc' else Documento.created_at.desc())
            
        query = query.paginate(page=page, per_page=per_page)

        return query.items, query.total, query.page, query.pages
    
    def get_documentos_empleado(empleado_id):
        """
        Obtiene todos los documentos asociados a un empleado.

        Args:
            empleado_id (int): Identificador del empleado.

        Returns:
            list: Lista de documentos asociados al empleado.
        """
        return Documento.query.filter_by(empleado_id=empleado_id).all()
    
    @classmethod
    def get_documentos_jinete(cls,jinete_id):
        """
        Obtiene todos los documentos asociados a un jinete.

        Args:
            jinete_id (int): Identificador del jinete.

        Returns:
            list: Lista de documentos asociados al jinete.
        """
        return cls.query.filter_by(jinete_id=jinete_id).all()