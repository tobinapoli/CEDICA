from datetime import datetime;
from src.core.database import db;

class MedioDePago(db.Model):
    """
    Modelo que representa un medio de pago en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        """
        Representación en forma de cadena del objeto MedioDePago.

        :return: Cadena que representa el medio de pago, incluyendo su ID y nombre.
        """
        return f'<MedioDePago #{self.id} nombre="{self.nombre}">'
    

    def get_nombre(self):
        """
        Obtiene el nombre del medio de pago.

        :return: Nombre del medio de pago.
        """
        return self.nombre
    
    def get_medios_de_pago():
        """
        Obtiene todos los medios de pago registrados en la base de datos.

        :return: Lista de objetos MedioDePago.
        """
        return MedioDePago.query.all()