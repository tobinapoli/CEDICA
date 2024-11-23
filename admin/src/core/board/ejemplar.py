from datetime import datetime
from src.core import board
from src.core.database import db
from sqlalchemy import desc, asc
from src.core.board.tipo_de_jinete import tipo_de_jinete
from enum import Enum
from copy import deepcopy

class tipo_adquisicion(Enum):
    """Enum para representar los tipos de adquisición de ejemplares."""
    compra = "compra"
    donacion = "donacion"

class ejemplar(db.Model):
    """Modelo que representa un ejemplar en la base de datos."""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    genero = db.Column(db.String(50))
    raza = db.Column(db.String(50))
    pela = db.Column(db.String(50))
    tipo_de_adquisicion = db.Column(db.Enum(tipo_adquisicion), nullable=False)
    fecha_ingreso = db.Column(db.Date)
    sede = db.Column(db.String(50))
    entrenadores = db.relationship('Empleado', secondary='empleado_ejemplar', backref='ejemplares')
    tipo_jinete = db.Column(db.Integer, db.ForeignKey('tipo_de_jinete.id'), nullable=True)
    documentos = db.relationship('Documento', backref='ejemplar', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    jinetes = db.relationship('JineteAmazona', backref='empleado', lazy=True)
    def __repr__(self):
        """Devuelve una representación en cadena del ejemplar.

        Returns:
            str: Representación en cadena del ejemplar.
        """
        return f'<Ejemplar #{self.id} nombre="{self.nombre}">'

    @staticmethod
    def list_ejemplar(filters=None, order_by=None, order_direction=None, page=1, per_page=25):
        """Lista ejemplares aplicando filtros y orden.

        Args:
            filters (dict, optional): Filtros a aplicar a la consulta.
            order_by (str, optional): Campo por el cual ordenar.
            order_direction (str, optional): Dirección de ordenamiento ('asc' o 'desc').

        Returns:
            list: Lista de ejemplares que coinciden con los filtros.
        """
        query = ejemplar.query
        if filters:
            if 'nombre' in filters and filters['nombre']:
                query = query.filter(ejemplar.nombre.like(f'%{filters["nombre"]}%'))
            if 'tipo_de_jinete' in filters and filters['tipo_de_jinete']:
                query = query.join(tipo_de_jinete).filter(tipo_de_jinete.nombre.ilike(f'%{filters["tipo_de_jinete"]}%'))

        if order_by:
            if order_direction == "desc":
                query = query.order_by(desc(order_by))  # Orden descendente
            else:
                query = query.order_by(asc(order_by))  # Orden ascendente
                
        paginated_query = query.paginate(page=page, per_page=per_page)
        return paginated_query.items, paginated_query.total, paginated_query.page, paginated_query.pages

    @staticmethod
    def get_ejemplar(id):
        """Obtiene un ejemplar por su ID.

        Args:
            id (int): Identificador del ejemplar.

        Returns:
            ejemplar: El ejemplar correspondiente al ID.
        """
        return ejemplar.query.get(id)

    @classmethod
    def create_ejemplar(cls, **kwargs):
        """Crea un nuevo ejemplar y lo agrega a la base de datos.

        Args:
            **kwargs: Atributos del ejemplar a crear.

        Returns:
            ejemplar: El ejemplar creado.
        """
        ejemplar = cls(
            nombre=kwargs["nombre"],
            fecha_nacimiento=kwargs["fecha_nacimiento"],
            genero=kwargs["genero"],
            raza=kwargs["raza"],
            pela=kwargs["pela"],
            tipo_de_adquisicion=kwargs["tipo_de_adquisicion"],
            fecha_ingreso=kwargs["fecha_ingreso"],
            sede=kwargs["sede"],
            entrenadores=kwargs["entrenadores"],
            tipo_jinete=kwargs["tipo_jinete"]
        )
        db.session.add(ejemplar)
        db.session.commit()
        return deepcopy(ejemplar)

    @staticmethod
    def update_ejemplar(id, **kwargs):
        """Actualiza un ejemplar existente.

        Args:
            id (int): Identificador del ejemplar a actualizar.
            **kwargs: Atributos del ejemplar a actualizar.

        Returns:
            ejemplar: El ejemplar actualizado.
        """
        ejemplar = board.ejemplar.query.get(id)
        for key, value in kwargs.items():
            if hasattr(ejemplar, key):
                setattr(ejemplar, key, value)
        db.session.commit()
        return deepcopy(ejemplar)

    @staticmethod
    def delete_ejemplar(id):
        """Elimina un ejemplar de la base de datos.

        Args:
            id (int): Identificador del ejemplar a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa.
        """
        ejemplar = board.ejemplar.query.get(id)
        db.session.delete(ejemplar)
        db.session.commit()
        return True

    @staticmethod
    def get_ejemplar_by_id(id):
        """Obtiene un ejemplar por su ID.

        Args:
            id (int): Identificador del ejemplar.

        Returns:
            ejemplar: El ejemplar correspondiente al ID.
        """
        return ejemplar.query.get(id)

    @staticmethod
    def get_documentos(ejemplar_id):
        """Obtiene los documentos asociados a un ejemplar.

        Args:
            ejemplar_id (int): Identificador del ejemplar.

        Returns:
            list[Documento]: Lista de documentos asociados al ejemplar.
        """
        return ejemplar.query.get(ejemplar_id).documentos
    
    @classmethod
    def get_all_ejemplar(cls):
        """
        Obtiene una lista de todos los ejemplares en la base de datos.

        Returns:
            list: Una lista de objetos Ejemplar que representan todos los ejemplares registrados.
        """
        return cls.query.all()