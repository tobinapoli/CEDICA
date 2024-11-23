from datetime import datetime;
from src.core.database import db;

class contacto_emergencia(db.Model):
    """
    Modelo de base de datos para un contacto de emergencia.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        """
        Devuelve una representación en cadena del contacto de emergencia.

        Returns:
            str: Representación del contacto de emergencia.
        """
        return f'<ContactoEmergencia #{self.id} nombre="{self.nombre}" telefono="{self.telefono}">'
    
    def create_contacto_emergencia(cls, **kwargs):
        """
        Crea un nuevo contacto de emergencia y lo almacena en la base de datos.

        Args:
            **kwargs: Parámetros del contacto de emergencia (nombre y teléfono).

        Returns:
            contacto_emergencia: El contacto de emergencia creado.
        """
        contacto = cls(
            nombre=kwargs["nombre"],
            telefono=kwargs["telefono"]
        )
        db.session.add(contacto)
        db.session.commit()
        return contacto
    
    
    @classmethod
    def get_contacto_emergencia(cls, id):
        """
        Recupera un contacto de emergencia por su identificador.

        Args:
            id (int): Identificador del contacto de emergencia a recuperar.

        Returns:
            contacto_emergencia: El contacto de emergencia correspondiente al ID, o None si no existe.
        """
        return  cls.query.get(id)
       
    
    
    @classmethod
    def update_contacto_emergencia(cls, id, **kwargs):
        """
        Actualiza un contacto de emergencia existente.

        Args:
            id (int): Identificador del contacto de emergencia a actualizar.
            **kwargs: Parámetros a actualizar (nombre y/o teléfono).

        Returns:
            contacto_emergencia: El contacto de emergencia actualizado.

        Raises:
            ValueError: Si el contacto de emergencia no se encuentra.
        """
        contacto = cls.get_contacto_emergencia(id)
        contacto.nombre = kwargs.get("nombre", contacto.nombre)
        contacto.telefono = kwargs.get("telefono", contacto.telefono)
        db.session.commit()
        return contacto