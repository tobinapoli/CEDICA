
from datetime import datetime;
from src.core.database import db;




class Rol(db.Model):
    """
    Modelo que representa un rol en el sistema.

    Atributos:
        id (int): Identificador único del rol.
        nombre (str): Nombre del rol.
        created_at (datetime): Fecha de creación del rol.
        updated_at (datetime): Fecha de la última actualización del rol.
        users (relationship): Relación con los usuarios asociados a este rol.
        permisos (relationship): Relación con los permisos asociados a este rol.
    """
    """
    Modelo que representa un rol en la base de datos.
    """
    __tablename__ = 'rol'  

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    users = db.relationship('User', back_populates='role')  
    permisos = db.relationship('Permiso', secondary='rol_permiso', back_populates='roles', lazy = 'joined')

    def __repr__(self):
        """
        Devuelve una representación legible del objeto Rol.

        Returns:
            str: Representación en formato '<Rol #ID nombre="nombre">'.
        """
        """
        Devuelve una representación en cadena del rol.

        :return: Una cadena que representa el rol, incluyendo su ID y nombre.
        """
        return f'<Rol #{self.id} nombre="{self.nombre}">'
    
    @classmethod
    def get_by_id(cls, rol_id):
        """
        Obtiene un rol por su ID.

        Args:
            rol_id (int): ID del rol a buscar.

        Returns:
            Rol or None: El rol si se encuentra, de lo contrario None.
        """
        """
        Obtiene un rol por su ID.

        :param rol_id: Identificador único del rol a buscar.
        :return: El rol correspondiente al ID, o None si no se encuentra.
        """
        return cls.query.get(rol_id)
    
    def create_role(**kwargs):
        """
        Crea un nuevo rol con los atributos proporcionados.

        Args:
            **kwargs: Los atributos del rol como argumentos clave-valor.

        Returns:
            Rol: La instancia del nuevo rol creado.

        """
        """
        Crea un nuevo rol en la base de datos.

        :args:
            **kwargs: Atributos del rol a crear (deben incluirse al menos 'nombre').
        
        :return: El rol creado.
        """
        role = Rol(**kwargs)
        db.session.add(role)
        db.session.commit()
        return role
    
    @classmethod   
    def get_all_role(self):
        """
        Obtiene todos los roles de la base de datos.

        :return: Lista de todos los roles en la base de datos.
        """
        rol = self.query.all()
        return rol

