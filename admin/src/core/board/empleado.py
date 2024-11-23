from datetime import datetime
from src.core.database import db
from src.core.board.puesto import Puesto
from copy import deepcopy

class Empleado(db.Model):
    """
    Modelo que representa a un empleado en la base de datos.
    
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    domicilio = db.Column(db.Integer, db.ForeignKey('domicilio.id'), nullable=False)
    documentos = db.relationship('Documento', backref='empleado', lazy=True)
    telefono = db.Column(db.String(50), nullable=False)
    puesto_id = db.Column(db.Integer, db.ForeignKey('puesto.id'), nullable=False)
    puesto = db.relationship('Puesto', backref='empleados', lazy='joined')
    profesion = db.Column(db.String(50), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False)
    fecha_egreso = db.Column(db.DateTime, nullable=True)
    contacto_emergencia_id = db.Column(db.Integer, db.ForeignKey('contacto_emergencia.id'), nullable=True)
    obra_social = db.Column(db.String(50), nullable=False)
    numero_afiliado = db.Column(db.String(50), nullable=False)
    condicion = db.Column(db.String(50), nullable=False)
    activo = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    
    jinetes_empleado = db.relationship('JineteAmazona', foreign_keys='JineteAmazona.profesor_id', back_populates='profesor_rel', overlaps="jinetes_auxiliar,jinetes_conductor")
    jinetes_auxiliar = db.relationship('JineteAmazona', foreign_keys='JineteAmazona.auxiliar_id', back_populates='auxiliar_rel', overlaps="jinetes_empleado,jinetes_conductor")
    jinetes_conductor = db.relationship('JineteAmazona', foreign_keys='JineteAmazona.conductor_id', back_populates='conductor_rel', overlaps="jinetes_empleado,jinetes_auxiliar")
    def __repr__(self):
        """
        Representación en formato string del objeto Empleado.
        
        :return: String con el ID, nombre y DNI del empleado.
        """
        return f'<Empleado #{self.id} nombre="{self.nombre}" dni="{self.dni}">'

    @classmethod
    def create_empleado(cls, **kwargs):
        """
        Crea un nuevo empleado en la base de datos.
        
        :param kwargs: Diccionario con los datos del empleado.
        :return: El empleado creado.
        """
        empleado = cls(
            nombre=kwargs["nombre"],  
            user_id=kwargs["user_id"], 
            apellido=kwargs["apellidos"],  
            dni=kwargs["dni"], 
            domicilio=kwargs["domicilio"], 
            email=kwargs["email"], 
            puesto_id=kwargs["puesto_id"], 
            telefono=kwargs["telefono"], 
            profesion=kwargs["profesion"], 
            fecha_ingreso=kwargs["fecha_ingreso"], 
            fecha_egreso=kwargs["fecha_egreso"], 
            contacto_emergencia_id=kwargs["contacto_emergencia_id"],  
            obra_social=kwargs["obra_social"], 
            numero_afiliado=kwargs["numero_afiliado"], 
            condicion=kwargs["condicion"], 
            activo=kwargs["activo"], 
        )
       
        db.session.add(empleado)
        db.session.commit()
        return deepcopy(empleado)

    def list_empleado(filters=None, order_by=None, order_direction="asc", page=1, per_page=25):
        """
        Lista los empleados aplicando filtros y ordenamiento.
        
        :param filters: Diccionario con filtros opcionales (nombre, apellido, dni, email, puesto).
        :param order_by: Campo por el cual ordenar los resultados (nombre, apellido, created_at).
        :param order_direction: Dirección del orden (asc o desc).
        :return: Lista de empleados.
        """
        query = Empleado.query

        if filters: 
            if 'nombre' in filters and filters['nombre']: 
                query = query.filter(Empleado.nombre.ilike(f"%{filters['nombre']}%"))
            if 'apellido' in filters and filters['apellido']: 
                query = query.filter(Empleado.apellido.ilike(f"%{filters['apellido']}%"))
            if 'dni' in filters and filters['dni']: 
                query = query.filter(Empleado.dni.ilike(f"%{filters['dni']}%")) 
            if 'email' in filters and filters['email']: 
                query = query.filter(Empleado.email.ilike(f"%{filters['email']}%")) 
            if 'puesto' in filters and filters['puesto']: 
                query = query.join(Puesto).filter(Puesto.nombre.ilike(f"%{filters['puesto']}%"))

        if order_by:
            direction = getattr(db, order_direction.lower(), db.asc)
            if order_by == 'nombre':
                query = query.order_by(direction(Empleado.nombre))
            elif order_by == 'apellido':
                query = query.order_by(direction(Empleado.apellido))
            elif order_by == 'created_at':
                query = query.order_by(direction(Empleado.created_at))
                
                
        paginated_query = query.paginate(page=page, per_page=per_page)
        return paginated_query
    

    def get_empleado(id):
        """
        Obtiene un empleado por su ID.
        
        :param id: ID del empleado.
        :return: Empleado encontrado con las fechas formateadas (si corresponde).
        """
        empleado = Empleado.query.get(id)
        empleado.fecha_ingreso = empleado.fecha_ingreso.strftime('%Y-%m-%d')
        if empleado.fecha_egreso:
            empleado.fecha_egreso = empleado.fecha_egreso.strftime('%Y-%m-%d')
        return empleado

    def update_empleado(id, **kwargs):
        """
        Actualiza un empleado existente con nuevos datos.
        
        :param id: ID del empleado.
        :param kwargs: Diccionario con los nuevos datos del empleado.
        :return: Empleado actualizado.
        """
        empleado = Empleado.query.get(id)
        if not empleado:
            return None  

        for key, value in kwargs.items():
            if hasattr(empleado, key):
                setattr(empleado, key, value)
        db.session.commit()  
        return empleado

    def delete_empleado(id):
        """
        Marca un empleado como inactivo.
        
        :param id: ID del empleado.
        """
        empleado = Empleado.query.get(id)
        empleado.activo = False
        db.session.commit()

    def show_empleado(id):
        """
        Muestra los detalles de un empleado por su ID.
        
        :param id: ID del empleado.
        :return: Empleado encontrado.
        """
        empleado = Empleado.query.get(id)
        return deepcopy(empleado)

    def get_empleado_by_dni(dni):
        """
        Obtiene un empleado por su DNI.
        
        :param dni: DNI del empleado.
        :return: Empleado encontrado.
        """
        empleado = Empleado.query.filter_by(dni=dni).first()
        return empleado

    def get_empleado_by_email(email):
        """
        Obtiene un empleado por su correo electrónico.
        
        :param email: Correo electrónico del empleado.
        :return: Empleado encontrado.
        """
        empleado = Empleado.query.filter_by(email=email).first()
        return empleado

    def get_empleado_by_numero_afiliado(numero_afiliado):
        """
        Obtiene un empleado por su número de afiliado.
        
        :param numero_afiliado: Número de afiliado del empleado.
        :return: Empleado encontrado.
        """
        empleado = Empleado.query.filter_by(numero_afiliado=numero_afiliado).first()
        return empleado
    
    def restore_empleado(id):
        """
        Restaura un empleado inactivo.
        
        :param id: ID del empleado.
        """
        empleado = Empleado.query.get(id)
        empleado.activo = True
        db.session.commit()

    def to_dict(self):
        """
        Convierte el objeto empleado a un diccionario.
        
        :return: Diccionario con los atributos del empleado.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_empleado_id(cls,id):
        return Empleado.query.filter_by(id=id).first()
    
    @classmethod
    def buscar_por_nombre(cls, query):
        """
        Busca empleados cuyos nombres coincidan con la consulta proporcionada.

        Args:
            query (str): La cadena que se usará para buscar en los nombres de los empleados.

        Returns:
            list: Una lista de objetos Empleado que coinciden con la búsqueda.
        """
        return cls.query.filter(cls.nombre.ilike(f'%{query}%')).all()
    
    @classmethod
    def get_all_empleado(cls):
        """
        Obtiene todos los empleados.

        Returns:
            list: Una lista de todos los objetos Empleado en la base de datos.
        """
        return cls.query.all()
        
    @classmethod
    def get_empleado_activos(cls):
        """
        Obtiene todos los empleados activos.

        Returns:
            list: Una lista de todos los objetos Empleado activos en la base de datos.
        """
        return cls.query.filter_by(activo=True).all()
        