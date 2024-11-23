
from enum import Enum
from src.core.board.jinete_amazona import JineteAmazona
from src.core.database import db;

class TipoEscolaridad(Enum):
    """
    Enumeración de los niveles de escolaridad.
    """
    primario = "Primario"
    secundario = "Secundario"
    terciario = "Terciario"
    universitario = "Universitario"

class FamiliarResponsable(db.Model):
    """
    Modelo que representa un familiar responsable de un jinete o amazona.
    """
    id = db.Column(db.Integer, primary_key=True)
    parentesco = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(50), nullable=False)
    domicilio = db.Column(db.Integer, db.ForeignKey('domicilio.id', ondelete = 'CASCADE'), nullable=False)
    celular = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    nivel_escolaridad = db.Column(db.Enum(TipoEscolaridad), nullable=False)
    actividad_ocupacion = db.Column(db.String(100), nullable=False)

    # Relación con Jinetes y Amazonas (muchos a muchos)
    jinetes_amazonas = db.relationship('JineteAmazona', secondary='jinete_familiar', back_populates='familiares_responsables')

    def __repr__(self):
        """
        Representa el objeto FamiliarResponsable como una cadena.

        Returns:
            str: Una representación legible del objeto, incluyendo su ID, nombre, apellido y DNI.
        """
        return f'<FamiliarResponsable #{self.id} nombre="{self.nombre}" apellido="{self.apellido}" fecha_nacimiento="{self.dni}" profesional_asociados="{self.email}" '
    
    @classmethod
    def create_familiar_responsable(cls, parentesco, nombre, apellido, dni, domicilio, celular, email, nivel_escolaridad, actividad_ocupacion, jinete_amazona_id):
        """
        Crea un nuevo familiar responsable y lo asocia a un jinete o amazona.

        Args:
            parentesco (str): Relación del familiar con el jinete.
            nombre (str): Nombre del familiar.
            apellido (str): Apellido del familiar.
            dni (str): Documento Nacional de Identidad del familiar.
            domicilio (int): Identificador del domicilio del familiar.
            celular (str): Número de teléfono celular del familiar.
            email (str): Correo electrónico del familiar.
            nivel_escolaridad (TipoEscolaridad): Nivel de escolaridad del familiar.
            actividad_ocupacion (str): Ocupación del familiar.
            jinete_amazona_id (int): Identificador del jinete o amazona.

        Returns:
            FamiliarResponsable: El objeto FamiliarResponsable creado.

        Raises:
            ValueError: Si el jinete ya tiene un familiar con el mismo DNI.
        """
        jinete = JineteAmazona.query.get(jinete_amazona_id)
        """
        Crea un nuevo FamiliarResponsable y lo asocia a un JineteAmazona.

        Parámetros:
        ----------
        - parentesco (str): Relación del familiar con el jinete/amazona.
        - nombre (str): Nombre del familiar.
        - apellido (str): Apellido del familiar.
        - dni (str): Documento Nacional de Identidad del familiar.
        - domicilio (int): ID del domicilio del familiar.
        - celular (str): Número de celular del familiar.
        - email (str): Correo electrónico del familiar.
        - nivel_escolaridad (TipoEscolaridad): Nivel educativo del familiar.
        - actividad_ocupacion (str): Actividad u ocupación del familiar.
        - jinete_amazona_id (int): ID del jinete/amazona al que se asociará el familiar.

        Retorna:
        --------
        FamiliarResponsable: El objeto creado del familiar responsable.

        Lanza:
        -------
        ValueError: Si el jinete ya tiene un familiar con el mismo DNI.

        Ejemplo de uso:
        ---------------
        ```python
        nuevo_familiar = FamiliarResponsable.create_familiar_responsable(
            parentesco="Madre", nombre="Ana", apellido="Pérez", dni="12345678",
            domicilio=1, celular="123456789", email="ana@example.com",
            nivel_escolaridad=TipoEscolaridad.primario, actividad_ocupacion="Ama de casa",
            jinete_amazona_id=1
        )
        ```
        """
        if any(familiar.dni == dni for familiar in jinete.familiares_responsables):
            raise ValueError(f'El jinete ya tiene un familiar con el DNI {dni}.')
        else:
            nuevo_familiar = cls(
                parentesco=parentesco,
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                domicilio=domicilio,
                celular=celular,
                email=email,
                nivel_escolaridad=nivel_escolaridad,
                actividad_ocupacion=actividad_ocupacion
            )

            jinete.familiares_responsables.append(nuevo_familiar)

            db.session.add(nuevo_familiar)
            db.session.commit()

            return nuevo_familiar
        
    @classmethod
    def update(cls, id, parentesco, nombre, apellido, dni, celular, email, nivel_escolaridad, actividad_ocupacion, domicilio_id):
        """
        Actualiza los atributos del FamiliarResponsable con los datos proporcionados.

        Args:
            id (int): Identificador del FamiliarResponsable a actualizar.
            parentesco (str): Nueva relación del familiar con el jinete.
            nombre (str): Nuevo nombre del familiar.
            apellido (str): Nuevo apellido del familiar.
            dni (str): Nuevo DNI del familiar.
            celular (str): Nuevo número de celular del familiar.
            email (str): Nuevo correo electrónico del familiar.
            nivel_escolaridad (TipoEscolaridad): Nuevo nivel de escolaridad del familiar.
            actividad_ocupacion (str): Nueva ocupación del familiar.
            domicilio_id (int): Nuevo identificador del domicilio del familiar.

        Raises:
            ValueError: Si no se encuentra el familiar responsable.
        """
        
        familiar_responsable = cls.query.get(id)
        if not familiar_responsable:
            raise ValueError(f"familiar responsable no encontrado.")
        familiar_responsable.parentesco = parentesco
        familiar_responsable.nombre = nombre
        familiar_responsable.apellido = apellido
        familiar_responsable.dni = dni
        familiar_responsable.celular = celular
        familiar_responsable.email = email
        familiar_responsable.nivel_escolaridad = nivel_escolaridad
        familiar_responsable.actividad_ocupacion = actividad_ocupacion
        familiar_responsable.domicilio = domicilio_id
        db.session.commit() 
        
    @classmethod
    def delete_all_by_jinete(cls, jinete_id):
        """
        Elimina todos los familiares responsables asociados a un JineteAmazona.

        Args:
            jinete_id (int): Identificador del jinete.

        Returns:
            None
        """
        familiares = cls.query.filter(cls.jinetes_amazonas.any(id=jinete_id)).all()
        for familiar in familiares:
            db.session.delete(familiar)  
        db.session.commit()  
    
    @classmethod
    def get_familiar(cls,id):
        """
        Obtiene un FamiliarResponsable por su ID.

        Args:
            id (int): Identificador del familiar responsable.

        Returns:
            FamiliarResponsable: El objeto FamiliarResponsable correspondiente al ID, o None si no se encuentra.
        """
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def delete_familiar(cls,id):
        """
        Elimina un FamiliarResponsable por su ID.

        Args:
            id (int): Identificador del familiar responsable a eliminar.

        Raises:
            ValueError: Si no se encuentra el familiar.
        """
        familiar = cls.query.filter_by(id=id).first()
        if familiar is None:
            raise ValueError("No existe ese familiar")
        db.session.delete(familiar)
        db.session.commit()
    