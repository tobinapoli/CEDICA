from datetime import datetime
from src.core.database import db

class Permiso(db.Model):
    """
    Modelo que representa a un permiso en la base de datos.
    """
    __tablename__ = 'permiso'

    id = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    roles = db.relationship('Rol', secondary='rol_permiso', back_populates='permisos')