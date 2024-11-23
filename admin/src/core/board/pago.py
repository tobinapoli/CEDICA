from datetime import datetime;
from src.core.database import db;
from src.core.board import Empleado


class Pago(db.Model):
    """
    Modelo que representa a un pago en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    beneficiario_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=True)
    beneficiario = db.relationship('Empleado', backref='pagos')
    tipo_de_pago = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @staticmethod
    def create_pago(beneficiario_id, monto, fecha, tipo_de_pago, descripcion):
        """
        Crea un nuevo pago en la base de datos.

        :args:
            beneficiario_id (int): ID del beneficiario asociado al pago (opcional).
            monto (float): Monto del pago.
            fecha (datetime): Fecha del pago.
            tipo_de_pago (str): Tipo de pago (e.g., "Honorarios").
            descripcion (str): Descripción del pago (opcional).
        
        :return: El pago creado.
        :raises ValueError: Si no se encuentra un beneficiario con el ID proporcionado.
        """
        if beneficiario_id:  
            beneficiario_obj = Empleado.query.get(beneficiario_id)
            if not beneficiario_obj:
                raise ValueError("No se encontró un beneficiario con ese ID.")
        else:
            beneficiario_obj = None  
        
        nuevo_pago = Pago(
            beneficiario=beneficiario_obj,
            monto=monto,
            fecha=fecha,
            tipo_de_pago=tipo_de_pago,
            descripcion=descripcion
        )
        db.session.add(nuevo_pago)
        db.session.commit()
        return nuevo_pago

    
    @classmethod
    def list_pagos(cls, filters=None, order_by='fecha', order_direction='asc', page=None, per_page=None):
        """
        Lista los pagos con los filtros y ordenamientos especificados.

        :args:
            filters (dict): Diccionario con los filtros a aplicar (opcional).
            order_by (str): Campo por el que se ordenarán los pagos (por defecto, 'fecha').
            order_direction (str): Dirección del orden (por defecto, 'asc').
            page (int): Número de página para paginación (opcional).
            per_page (int): Número de pagos por página (opcional).
        
        :return: Lista de pagos filtrados y ordenados.
        """
        query = cls.query
        
        # Aplicar filtros
        if filters.get('beneficiario'):
            query = query.join(cls.beneficiario).filter(
            (Empleado.nombre.ilike(f"%{filters['beneficiario']}%")) |
            (Empleado.apellido.ilike(f"%{filters['beneficiario']}%"))
            )
        if filters.get('tipo_de_pago'):
            query = query.filter(cls.tipo_de_pago == filters['tipo_de_pago'])
        if filters.get('fecha_inicio'):
            query = query.filter(cls.fecha >= filters['fecha_inicio'])
        if filters.get('fecha_fin'):
            query = query.filter(cls.fecha <= filters['fecha_fin'])

        if filters.get('beneficiario'):
            query = query.filter(cls.tipo_de_pago == 'Honorarios')
            
        # Ordenar resultados
        if order_direction == 'desc':
            query = query.order_by(db.desc(getattr(cls, order_by)))
        else:
            query = query.order_by(getattr(cls, order_by))
            
        if page and per_page:
            pagos = query.paginate(page=page, per_page=per_page)
        else:
            pagos = query.all()

        return pagos

    
    def count_pagos(cls,filters=None):
        """
        Cuenta la cantidad de pagos existentes aplicando filtros.

        :args:
            filters (dict): Diccionario con los filtros a aplicar (opcional).
        
        :return: Cantidad de pagos que coinciden con los filtros.
        """
        query = cls.query
        if filters.get('beneficiario'):
            query = query.join(cls.beneficiario).filter(
            (Empleado.nombre.ilike(f"%{filters['beneficiario']}%")) |
            (Empleado.apellido.ilike(f"%{filters['beneficiario']}%"))
            )
        if filters.get('tipo_de_pago'):
            query = query.filter(cls.tipo_de_pago == filters['tipo_de_pago'])
        if filters.get('fecha_inicio'):
            query = query.filter(cls.fecha >= filters['fecha_inicio'])
        if filters.get('fecha_fin'):
            query = query.filter(cls.fecha <= filters['fecha_fin'])

        if filters.get('beneficiario'):
            query = query.filter(cls.tipo_de_pago == 'Honorarios')
        return query.count()

    
    @classmethod
    def get_tipos_de_pago(cls):
        """
        Obtiene los tipos de pago existentes en la base de datos.

        :return: Lista de tipos de pago distintos.
        """
        return db.session.query(cls.tipo_de_pago).distinct().all()
    
    
    @staticmethod
    def get_pago_by_fecha_beneficiario(fecha, beneficiario_id, tipo_de_pago, monto):
        """
        Compara si todos los campos son iguales para el chequeo de pagos repetidos.

        :args:
            fecha (datetime): Fecha del pago.
            beneficiario_id (int): ID del beneficiario asociado.
            tipo_de_pago (str): Tipo de pago (e.g., "Honorarios").
            monto (float): Monto del pago.
        
        :return: El pago que coincide con los criterios, si existe.
        :raises ValueError: Si se solicita un beneficiario para pagos de tipo 'Honorarios' sin proporcionar uno.
        """
        query = Pago.query.filter(
            Pago.fecha == fecha,
            Pago.tipo_de_pago == tipo_de_pago,
            Pago.monto == monto
        )

        if tipo_de_pago == "Honorarios":
            if beneficiario_id:
                query = query.filter(Pago.beneficiario_id == beneficiario_id)
            else:
                raise ValueError("Debe proporcionar un beneficiario para pagos de tipo 'Honorarios'.")

        return query.first()

    
    @staticmethod
    def get_pago(id):
        """
        Obtiene un pago mediante su ID.

        :args:
            id (int): ID del pago.
        
        :return: El pago correspondiente al ID, o None si no se encuentra.
        """
        return Pago.query.get(id)
    
    
    @classmethod
    def update_pago(cls, id, beneficiario_id, monto, fecha, tipo_de_pago, descripcion):
        """
        Actualiza un pago existente.

        :args:
            id (int): ID del pago a actualizar.
            beneficiario_id (int): ID del beneficiario asociado (opcional).
            monto (float): Nuevo monto del pago.
            fecha (datetime): Nueva fecha del pago.
            tipo_de_pago (str): Nuevo tipo de pago.
            descripcion (str): Nueva descripción del pago (opcional).
        
        :return: El pago actualizado, o None si no se encuentra.
        """
        pago = cls.query.get(id)
        if not pago:
            return None  
        pago.monto = monto
        pago.fecha = datetime.strptime(fecha, '%Y-%m-%d')  
        pago.tipo_de_pago = tipo_de_pago
        pago.descripcion = descripcion
        
        if tipo_de_pago == 'Honorarios':
            if beneficiario_id:  
                beneficiario_obj = Empleado.query.get(beneficiario_id)
            pago.beneficiario = beneficiario_obj
        else:
            pago.beneficiario = None  

        try:
            db.session.commit()
            return pago
        except Exception as e:
            db.session.rollback()  
            raise e
        
    @classmethod
    def delete_pago(cls, id):
        """
        Elimina un pago existente.

        :args:
            id (int): ID del pago a eliminar.
        
        :return: True si se eliminó correctamente, None si no se encontró el pago.
        """
        pago = cls.query.get(id)
        if not pago:
            return None  

        try:
            db.session.delete(pago)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()  
            raise e    