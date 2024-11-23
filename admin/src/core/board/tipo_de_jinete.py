from datetime import datetime;
from src.core.database import db;

class tipo_de_jinete(db.Model):
    """
    Modelo que representa un tipo de jinete en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        """
        Devuelve una representación en cadena del tipo de jinete.

        :return: Una cadena que representa el tipo de jinete, incluyendo su ID y nombre.
        """
        return f'<tipo_de_jinete #{self.id} - {self.nombre}>'
    
    def list_tipo_de_jinete():
        """
        Lista todos los tipos de jinete en la base de datos.

        :return: Una lista de todos los tipos de jinete.
        """
        return tipo_de_jinete.query.all()