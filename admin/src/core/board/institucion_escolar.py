from src.core.database import db

class InstitucionEscolar(db.Model):
    """
    Modelo que representa una Institución Escolar.

    Atributos:
    ----------
    id : int
        Identificador único de la institución escolar.
    nombre : str
        Nombre de la institución escolar.
    direccion : str
        Dirección de la institución escolar.
    telefono : str, opcional
        Número de teléfono de la institución escolar.
    observaciones : str, opcional
        Observaciones adicionales sobre la institución escolar.
    jinetes : list
        Relación con los jinetes/amazonas asociados a la institución.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(50), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    jinetes = db.relationship('JineteAmazona', backref='institucion_escolar', lazy=True)

    def __repr__(self):
        return f'<InstitucionEscolar #{self.id} nombre="{self.nombre}">'
    
    @classmethod
    def create_institucion_escolar(cls, nombre, direccion, telefono, observaciones):
        """Crea una nueva Institución Escolar."""
        nueva_institucion = cls(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            observaciones=observaciones
        )
        db.session.add(nueva_institucion)
        db.session.commit()
        return nueva_institucion
    
    @classmethod
    def delete_institucion_escolar(cls,id):
        school = cls.query.get(id)
        if school is None:
            raise ValueError("No se encontro una escuela con ese ID")
        db.session.delete(school)
        db.session.commit()
        
    @classmethod
    def update_institucion_escolar(cls, id, nombre, direccion, telefono=None, observaciones=None):
        # Buscar la institución escolar por ID
        institucion_escolar = cls.query.get(id)
        
        if not institucion_escolar:
            raise ValueError(f"Institución escolar con ID {id} no encontrada.")

        # Actualizar los campos
        institucion_escolar.nombre = nombre or institucion_escolar.nombre
        institucion_escolar.direccion = direccion or institucion_escolar.direccion
        institucion_escolar.telefono = telefono or institucion_escolar.telefono
        institucion_escolar.observaciones = observaciones or institucion_escolar.observaciones

        # Guardar los cambios
        db.session.commit()

        return institucion_escolar
    
    @classmethod
    def get_institucion_escolar(cls, id):
        # Buscar institución escolar por ID
        institucion_escolar = cls.query.get(id)
        
        if not institucion_escolar:
            raise ValueError(f"Institución escolar con ID {id} no encontrada.")
        
        # Retornar los datos de la institución escolar como un diccionario
        return institucion_escolar