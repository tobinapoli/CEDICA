from datetime import datetime;
from src.core.database import db;

class Puesto(db.Model):
    """
    Modelo que representa un puesto en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        """
        Devuelve una representación en cadena del puesto.

        :return: Una cadena que representa el puesto, incluyendo su ID y nombre.
        """
        return f'<Profesion #{self.id} nombre="{self.nombre}>'
    
    def create_puesto(**kwargs):
        """
        Crea un nuevo puesto en la base de datos.

        :args:
            **kwargs: Atributos del puesto a crear (deben incluirse al menos 'nombre').
        
        :return: El puesto creado.
        """
        profesion = Puesto(**kwargs)
        db.session.add(profesion)
        db.session.commit()
        return profesion
    
    def list_puesto(filters=None, order_by=None, order_direction="asc"):
        """
        Lista los puestos en la base de datos, aplicando filtros y ordenamientos si se especifican.

        :args:
            filters (dict): Diccionario con filtros a aplicar (opcional).
            order_by (str): Campo por el cual se ordenarán los puestos (opcional).
            order_direction (str): Dirección del orden ('asc' o 'desc', por defecto 'asc').
        
        :return: Lista de puestos filtrados y ordenados.
        """
        query = Puesto.query
        if filters:
            if 'nombre' in filters and filters['nombre']:
                query = query.filter(Puesto.nombre.like(f"%{filters['nombre']}%"))
        if order_by:
            query = query.order_by(order_by + " " + order_direction)
        return query.all()
    
    def get_puestos():
        """
        Obtiene todos los puestos de la base de datos.

        :return: Lista de todos los puestos.
        """
        return Puesto.query.all()