from datetime import datetime
from src.core import board
from src.core.database import db
from sqlalchemy import desc, asc
from src.core.board.tipo_de_jinete import tipo_de_jinete
from enum import Enum
from src.core.auth import User

class Estado(Enum):
    """Enum para representar los estados de un contenido."""
    publicado = "Publicado"
    borrador = "Borrador"
    archivado = "Archivado"

class Contenido(db.Model):
    """Modelo que representa un contenido en la base de datos."""
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(130), nullable=False)
    copete = db.Column(db.String(350), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    autor = db.relationship('User', backref='contenidos')
    fecha_publicacion = db.Column(db.Date, nullable=True)
    estado = db.Column(db.Enum(Estado), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    @classmethod 
    def __repr__(self):
        """Devuelve una representación en cadena del contenido.

        Returns:
            str: Representación en cadena del contenido.
        """
        return f'<Contenido #{self.id} titulo="{self.titulo}">'

    @classmethod
    def list_contenido(cls, page, per_page, filters=None, sort_by=None, order='asc'):
        query = Contenido.query
        
        # Filtrado
        if filters:
            if 'titulo' in filters and filters['titulo']:
                query = query.filter(Contenido.titulo.ilike(f"%{filters['titulo']}%"))
            if 'autor' in filters and filters['autor']:
                query = query.join(User).filter(User.alias.ilike(f"%{filters['autor']}%"))
            if 'estado' in filters and filters['estado']:
                estado_enum = Estado[filters['estado']] if filters['estado'] in Estado.__members__ else None
                if estado_enum:
                    query = query.filter(Contenido.estado == estado_enum)

        # Ordenación
        if not sort_by:
                sort_by = 'created_at'
        if order == 'desc':
            query = query.order_by(desc(sort_by))
        else:
            query = query.order_by(asc(sort_by))
        return query.paginate(page=page, per_page=per_page)
        
        

    @classmethod
    def create_contenido(cls, titulo, copete, contenido, user_email, fecha_publicacion, estado):
        autor = User.query.filter(User.email == user_email).first()
        
        
        contenido = cls(
            titulo=titulo,
            copete=copete,
            contenido=contenido,
            autor_id=autor.id,
            autor=autor,
            fecha_publicacion=fecha_publicacion,
            estado=estado
        )
        db.session.add(contenido)
        db.session.commit()
        return contenido
        

    def update_contenido( id,titulo, copete, contenido, autor):
        """Actualiza un contenido en la base de datos.

        Args:
            kwargs (dict): Datos del contenido a actualizar.
        """
        contenidoAux = Contenido.query.get(id)
        autorAux = User.query.filter(User.id == autor).first()
        contenidoAux.titulo = titulo
        contenidoAux.copete = copete
        contenidoAux.contenido = contenido
        contenidoAux.autor = autorAux
        contenidoAux.updated_at = datetime.now()
        contenidoAux.autor_id = autorAux.id
    
        db.session.commit()
        
    def delete_contenido(id):
        """Elimina un contenido de la base de datos."""
        contenido = Contenido.get_contenido(Contenido,id)
        db.session.delete(contenido)
        db.session.commit()
        
    def archivar_contenido(self):
        """Archiva un contenido."""
        self.estado = Estado.archivado
        self.updated_at = datetime.now()
        db.session.commit()
        
    def publicar_contenido(self):
        """Publica un contenido."""
        self.estado = Estado.publicado
        self.fecha_publicacion = datetime.now().date()
        self.updated_at = datetime.now()
        db.session.commit()
        
    def get_contenido(cls, id):
        """Obtiene un contenido por su identificador.

        Args:
            id (int): Identificador del contenido a obtener.

        Returns:
            Contenido: Contenido obtenido.
        """
        return cls.query.get(id)
    
    def publicar_contenido(cls, id):
        """Publica un contenido por su identificador.

        Args:
            id (int): Identificador del contenido a publicar.
        """
        contenido = cls.query.get(id)
        contenido.estado = Estado.publicado
        contenido.fecha_publicacion = datetime.now().date()
        db.session.commit()
        
    def archivar_contenido(cls, id):
        """Archiva un contenido por su identificador.

        Args:
            id (int): Identificador del contenido a archivar.
        """
        contenido = cls.query.get(id)
        contenido.estado = Estado.archivado
        db.session.commit()

    

    
