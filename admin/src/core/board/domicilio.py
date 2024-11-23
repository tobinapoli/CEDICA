from datetime import datetime;
from src.core.database import db;

from enum import Enum

class TipoProvincia(Enum):
    """
    Enumeración de las provincias argentinas y las Islas Malvinas.
    """
    BUENOS_AIRES = "Buenos Aires"
    CIUDAD_AUTONOMA_BUENOS_AIRES = "Ciudad Autónoma de Buenos Aires"
    CATAMARCA = "Catamarca"
    CHACO = "Chaco"
    CHUBUT = "Chubut"
    CORDOBA = "Córdoba"
    CORRIENTES = "Corrientes"
    ENTRE_RIOS = "Entre Ríos"
    FORMOSA = "Formosa"
    JUJUY = "Jujuy"
    LA_PAMPA = "La Pampa"
    LA_RIOJA = "La Rioja"
    MENDOZA = "Mendoza"
    MISIONES = "Misiones"
    NEUQUEN = "Neuquén"
    RIO_NEGRO = "Río Negro"
    SALTA = "Salta"
    SAN_JUAN = "San Juan"
    SAN_LUIS = "San Luis"
    SANTA_FE = "Santa Fe"
    SANTA_CRUZ = "Santa Cruz"
    SANTIAGO_DEL_ESTERO = "Santiago del Estero"
    TIERRA_DEL_FUEGO = "Tierra del Fuego"
    ISLAS_MALVINAS = "Islas Malvinas"
    
class domicilio(db.Model):
    """
    Modelo de base de datos para representar un domicilio.
    """
    id = db.Column(db.Integer, primary_key=True)
    calle = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    depto = db.Column(db.String(10), nullable=True)
    localidad = db.Column(db.String(50), nullable=False)
    provincia = db.Column(db.Enum(TipoProvincia), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        """
        Devuelve una representación en cadena del domicilio.

        Returns:
            str: Representación del domicilio, incluyendo su calle y número.
        """
        return f'<Domicilio #{self.id} calle="{self.calle}" numero="{self.numero}">'
    
    
    @classmethod 
    def list_domicilio():
        """
        Obtiene una lista de todos los domicilios en la base de datos.

        Returns:
            list: Lista de objetos Domicilio.
        """
        domicilios = domicilio.query.all()
        return domicilios
    
    def create_domicilio(cls, **kwargs):
        """
        Crea un nuevo domicilio y lo guarda en la base de datos.

        Args:
            kwargs (dict): Parámetros del domicilio a crear, que incluyen
                           'calle', 'numero', 'depto', 'localidad' y 'provincia'.

        Returns:
            Domicilio: El domicilio creado.
        """
        domicilio = cls( 
            calle=kwargs["calle"],
            numero=kwargs["numero"],
            depto=kwargs.get("depto"),
            localidad=kwargs["localidad"],
            provincia=kwargs["provincia"]
        )
        db.session.add(domicilio)
        db.session.commit()
        return domicilio
    
    @classmethod
    def get_domicilio(cls, id):
        """
        Obtiene un domicilio específico por su identificador.

        Args:
            id (int): Identificador del domicilio.

        Returns:
            Domicilio: El domicilio correspondiente al id dado o None si no se encuentra.
        """
        return cls.query.get(id)
    
    @classmethod
    def update_domicilio(cls, id, **kwargs):
        """
        Actualiza un domicilio existente.

        Args:
            id (int): Identificador del domicilio a actualizar.
            kwargs (dict): Parámetros a actualizar en el domicilio.

        Returns:
            Domicilio: El domicilio actualizado.
        """
        domicilio = cls.get_domicilio(id)
        domicilio.calle = kwargs.get("calle", domicilio.calle) 
        domicilio.numero = kwargs.get("numero", domicilio.numero) 
        domicilio.depto = kwargs.get("depto", domicilio.depto) 
        domicilio.localidad = kwargs.get("localidad", domicilio.localidad) 
        domicilio.provincia = kwargs.get("provincia", domicilio.provincia) 
        db.session.commit()
        return domicilio