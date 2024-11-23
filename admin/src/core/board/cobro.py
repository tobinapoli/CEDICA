from copy import deepcopy
from datetime import datetime;
from src.core import board
from src.core.database import db;
from src.core.board.jinete_amazona import JineteAmazona;
from src.core.board.medio_de_pago import MedioDePago;
from src.core.board import Empleado
from sqlalchemy import or_, and_
from sqlalchemy.orm import aliased

class cobro(db.Model):
    """
    Modelo de base de datos para un cobro realizado a un jinete amazona.
    """
    id = db.Column(db.Integer, primary_key=True)
    jinetes = db.Column(db.Integer, db.ForeignKey('jinete_amazona.id', ondelete='CASCADE'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    medio_de_pago = db.Column(db.Integer, db.ForeignKey('medio_de_pago.id'), nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    observaciones = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    jinete_amazona = db.relationship('JineteAmazona', backref=db.backref('cobros', cascade="all, delete-orphan"))

    def __repr__(self):
        """
        Devuelve una representación en cadena del cobro.

        Returns:
            str: Representación del cobro, incluyendo su ID, monto y fecha.
        """
        return f'<cobro #{self.id} monto="{self.monto} fecha="{self.fecha}>'
        
    @classmethod
    def create_cobro(cls, **kwargs):
        """
        Crea un nuevo registro de cobro en la base de datos.

        Parámetros:
        -----------
        - kwargs (dict): Diccionario de argumentos que incluye:
            - jinetes (int): ID del jinete asociado.
            - fecha (datetime): Fecha del cobro.
            - monto (float): Monto del cobro.
            - medio_de_pago (int): ID del medio de pago utilizado.
            - empleado_id (int): ID del empleado que realiza el cobro.
            - observaciones (str): Observaciones adicionales para el cobro.

        Retorna:
        --------
        - Cobro: El cobro creado.

        Excepciones:
        -----------
        - Puede lanzar una excepción si hay un error al agregar el cobro a la base de datos o al cometer la transacción.
        """
        cobro = cls(
            jinetes=kwargs["jinetes"],
            fecha=kwargs["fecha"],
            monto=kwargs["monto"],
            medio_de_pago=kwargs["medio_de_pago"],
            empleado_id=kwargs["empleado_id"],
            observaciones=kwargs["observaciones"]
        )
        db.session.add(cobro)
        db.session.commit()
        return cobro
    
    
    def get_cobro(id):
        """
        Obtiene un registro de cobro específico desde la base de datos.

        Parámetros:
        -----------
        - id (int): El ID del cobro a obtener.

        Retorna:
        --------
        - Cobro: El cobro dada la ID especificada.
        - None: Si no se encuentra un cobro con el ID especificado.
        """
        cobroX = cobro.query.get(id)
        return cobroX
    
    def update_cobro(id, **kwargs):
        """
        Actualiza los campos especificados de un registro de cobro existente.

        Parámetros:
        -----------
        - id (int): El ID del cobro a actualizar.
        - kwargs (dict): Diccionario de campos y valores a actualizar en el cobro. 
                        Los nombres de los campos deben coincidir con los atributos del modelo.

        Retorna:
        --------
        - Cobro: El objeto `cobro` actualizado.
        - None: Si no se encuentra un cobro con el ID especificado.
        """
        cobroX = cobro.query.get(id)
        if not cobroX:
            return None  

        for key, value in kwargs.items():
            if hasattr(cobroX, key):
                setattr(cobroX, key, value)
        db.session.commit() 
        return cobroX

    def existe_jinete(jinete_id):
        """
        Verifica la existencia de cobros asociados a un jinete específico.

        Parámetros:
        -----------
        - jinete_id (int): ID del jinete que se desea verificar.

        Retorna:
        --------
        - bool: `True` si existen cobros relacionados con el jinete, `False` en caso contrario.
        """
        return db.session.query(cobro).filter(cobro.jinetes == jinete_id).count() > 0

    def get_cobros_filtro(filters=None , order_by=None, order_direction=None, page=None, per_page=None, jinete_id=None): 
        """
        Obtiene una lista de cobros aplicando filtros, ordenación y paginación.

        Parámetros:
        -----------
        - filters (dict): Filtros a aplicar en la consulta, tales como `fechaMin`, `fechaMax`, 
                        `medio_de_pago`, `empleado.nombre` y `empleado.apellido`.
        - order_by (str): Campo para ordenar la consulta, predeterminado en `fecha`.
        - order_direction (str): Dirección de ordenación, `asc` o `desc`.
        - page (int): Número de página para la paginación.
        - per_page (int): Número de registros por página.
        - jinete_id (int): ID del jinete para filtrar cobros específicos.

        Retorna:
        --------
        - Paginacion: Objeto de paginación de cobros si se proporciona `page` y `per_page`.
        """

        query = db.session.query(board.Cobro, Empleado, MedioDePago).join(Empleado).join(MedioDePago)\
        .filter(board.Cobro.jinetes == jinete_id)


        if filters:
            if filters['fechaMin']: 
                query = query.filter(board.Cobro.fecha >= filters['fechaMin'])
        
            if filters['fechaMax']:  
                query = query.filter(board.Cobro.fecha <= filters['fechaMax'])
            
            if filters['medio_de_pago']: 
                query = query.filter(board.Cobro.medio_de_pago == filters['medio_de_pago']) 
            
            if filters['empleado.nombre']:
                query = query.filter(Empleado.nombre.ilike(f"%{filters['empleado.nombre']}%"))
            
            if filters['empleado.apellido']:
                query = query.filter(Empleado.apellido.ilike(f"%{filters['empleado.apellido']}%"))
        

        if order_by:
            direction = getattr(db, order_direction.lower(), db.asc) 
            if order_by == 'fecha':  
                query = query.order_by(direction(board.Cobro.fecha))
        
        cobros = query.paginate(page=page, per_page=per_page)
            
        return cobros

    def obtener_medio_pago(id):
        """
        Obtiene un registro de MedioDePago específico basado en el ID.

        Parámetros:
        -----------
        - id (int): ID del medio de pago a obtener.

        Retorna:
        --------
        - MedioDePago: Objeto de medio de pago correspondiente al ID, o `None` si no existe.
        """
        medio_de_pago = MedioDePago.query.get(id)
        return medio_de_pago
    
    def obtener_empleado(id):
        """
        Obtiene un registro de Empleado específico basado en el ID.

        Parámetros:
        -----------
        - id (int): ID del empleado a obtener.

        Retorna:
        --------
        - Empleado: Objeto de empleado correspondiente al ID, o `None` si no existe.
        """
        empleado = Empleado.query.get(id)
        return empleado
        
    def delete_cobro(id):
        """
        Elimina un cobro específico de la base de datos basado en el ID.

        Parámetros:
        -----------
        - id (int): ID del cobro a eliminar.

        Retorna:
        --------
        - None
        """
        cobroX = cobro.query.get(id)
        db.session.delete(cobroX)
        db.session.commit()
        
    @classmethod
    def get_cobros(cls, fecha_inicio, fecha_fin, jinete_nombre, jinete_dni):
        query = cls.query


        if fecha_inicio:
            query = query.filter(cls.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(cls.fecha <= fecha_fin)

        if jinete_nombre:
            query = query.join(JineteAmazona).filter(
                and_(
                    JineteAmazona.nombre.ilike(f'%{jinete_nombre}%'),
                )
            )
        
        if jinete_dni:
            query = query.join(JineteAmazona).filter(JineteAmazona.dni == jinete_dni)

        return query.all()


        