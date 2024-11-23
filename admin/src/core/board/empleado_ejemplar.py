from src.core.database import db;
from datetime import datetime;

class EmpleadoEjemplar(db.Model):
    """
    Modelo que representa la relación entre un empleado y un ejemplar.
    """
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    ejemplar_id = db.Column(db.Integer, db.ForeignKey('ejemplar.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        """
        Devuelve una representación en cadena del objeto EmpleadoEjemplar.

        Returns:
            str: Representación en cadena que incluye el id, el empleado_id y el ejemplar_id.
        """
        return f'<EmpleadoEjemplar #{self.id} empleado_id="{self.empleado_id}" ejemplar_id="{self.ejemplar_id}>'