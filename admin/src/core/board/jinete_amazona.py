
from datetime import datetime
from enum import Enum
from src.core.board.domicilio import TipoProvincia
from src.core.board.domicilio import TipoProvincia
from src.core.board import situacion_previsional
from src.core.board.situacion_previsional import SituacionPrevisional
from src.core.database import db
from sqlalchemy import func


class TipoSede(Enum):
    """
    Enumeración para los tipos de sede.
    """
    CASJ = "CASJ"
    HLP = "HLP"
    Otro = "Otro"
    
class TipoCondicion(Enum):
    """
    Enumeración para las condiciones de los jinetes/amazonas.
    """
    Regular = "Regular"
    De_baja = "De baja"

class TipoPropuesta(Enum):
    """
    Enumeración para los tipos de propuestas de trabajo.
    """
    HIPOTERAPIA = "Hipoterapia"
    MONTA_TERAPEUTICA = "Monta Terapéutica"
    DEPORTE_ECUESTRE_ADAPTADO = "Deporte Ecuestre Adaptado"
    ACTIVIDADES_RECREATIVAS = "Actividades Recreativas"
    EQUITACION = "Equitación"

class TipoPension(Enum):
    """
    Enumeración para los tipos de pensión.
    """
    Nacional = "Nacional"
    Provincial = "Provincial"
    
class TipoAsignacion(Enum):
    """
    Enumeración para los tipos de asignación familiar.
    """
    AUH = "Asignación Universal por hijo"
    AUHD = "Asignación Universal por hijo con Discapacidad"
    AAE = "Asignación por ayuda escolar anual"
    
    
class TipoDiscapacidad(Enum):
    """
    Enumeración para los tipos de discapacidad.
    """
    Mental = "Mental"
    Motora = "Motora"
    Sensorial = "Sensorial"
    Visceral = "Visceral"
    


    
jinete_familiar = db.Table('jinete_familiar',
    db.Column('jinete_amazona_id', db.Integer, db.ForeignKey('jinete_amazona.id', ondelete='CASCADE'), primary_key=True),
    db.Column('familiar_responsable_id', db.Integer, db.ForeignKey('familiar_responsable.id', ondelete='CASCADE'), primary_key=True)
)


class JineteAmazona(db.Model):
    """
    Modelo que representa un jinete/amazona.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    tiene_deuda = db.Column(db.Boolean, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    localidad_nacimiento = db.Column(db.String(50), nullable=False)
    provincia_nacimiento = db.Column(db.Enum(TipoProvincia), nullable = False)
    dni = db.Column(db.String(50), unique=True, nullable=False, index=True)
    domicilio = db.Column(db.Integer, db.ForeignKey('domicilio.id', ondelete = 'CASCADE'), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    contacto_emergencia_id = db.Column(db.Integer, db.ForeignKey('contacto_emergencia.id', ondelete = 'CASCADE'), nullable=True)
    becado = db.Column(db.Boolean, nullable=False, default = False)
    porcentaje_beca = db.Column(db.Integer, nullable=True)
    profesionales_asociados = db.Column(db.String(50), nullable=False)
    certificado_discapacidad = db.Column(db.Boolean, nullable=False, default=False) 
    diagnostico_discapacidad = db.Column(db.String(50), nullable=True)
    tipo_discapacidad = db.Column(db.Enum(TipoDiscapacidad), nullable = True)
    asignacion_familiar = db.Column(db.Boolean, nullable= False)
    tipo_asignacion = db.Column(db.Enum(TipoAsignacion), nullable = True)
    pensionado = db.Column(db.Boolean, nullable = False)
    tipo_pension = db.Column(db.Enum(TipoPension), nullable = True)
    situacion_previsional_id = db.Column(db.Integer, db.ForeignKey('situacion_previsional.id', ondelete = 'CASCADE'), nullable=True)
    institucion_escolar_id = db.Column(db.Integer, db.ForeignKey('institucion_escolar.id', ondelete = 'CASCADE'), nullable=True)
    grado_actual = db.Column(db.String(50), nullable = True)  
    propuesta_trabajo = db.Column(db.Enum(TipoPropuesta), nullable = False)
    condicion = db.Column(db.Enum(TipoCondicion), nullable = False)
    sede = db.Column(db.Enum(TipoSede), nullable = False)
    dias_trabajo = db.Column(db.ARRAY(db.String), nullable=True) 

    
    profesor_id = db.Column(db.Integer, db.ForeignKey('empleado.id', ondelete='SET NULL'), nullable=True)
    profesor_rel = db.relationship('Empleado', foreign_keys=[profesor_id], back_populates='jinetes_empleado')

    auxiliar_id = db.Column(db.Integer, db.ForeignKey('empleado.id', ondelete='SET NULL'), nullable=True)
    auxiliar_rel = db.relationship('Empleado', foreign_keys=[auxiliar_id], back_populates='jinetes_auxiliar')

    conductor_id = db.Column(db.Integer, db.ForeignKey('empleado.id', ondelete='SET NULL'), nullable=True)
    conductor_rel = db.relationship('Empleado', foreign_keys=[conductor_id], back_populates='jinetes_conductor')
    
    caballo_id = db.Column(db.Integer, db.ForeignKey('ejemplar.id', ondelete='SET NULL'), nullable=True)
    

    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    documentos = db.relationship('Documento', backref='jinete_amazona', lazy=True)
    situacion_previsional = db.relationship('SituacionPrevisional', back_populates='jinetes_amazonas')
    familiares_responsables = db.relationship('FamiliarResponsable', secondary=jinete_familiar, back_populates='jinetes_amazonas')
    
    
    
    
    def __repr__(self):
        """
        Representa una instancia de JineteAmazona como una cadena.

        :return: Cadena que representa al jinete/amazona con su ID, nombre, apellido y DNI.
        """
        return (f'<JineteAmazona #{self.id} '
            f'nombre="{self.nombre}" '
            f'apellido="{self.apellido}" '
            f'dni="{self.dni}" '
            f'domicilio="{self.domicilio}" '
            f'tiene_deuda="{self.tiene_deuda}" '
            f'becado="{self.becado}" '
            f'telefono="{self.telefono}" '
            f'fecha_nacimiento="{self.fecha_nacimiento}" '
            f'contacto_emergencia_id="{self.contacto_emergencia_id}" '
            f'profesionales_asociados="{self.profesionales_asociados}" '
            f'certificado_discapacidad="{self.certificado_discapacidad}" '
            f'asignacion_familiar="{self.asignacion_familiar}" '
            f'pensionado="{self.pensionado}" '
            f'situacion_previsional_id="{self.situacion_previsional_id}" '
            f'porcentaje_beca="{self.porcentaje_beca}" '
            f'diagnostico_discapacidad="{self.diagnostico_discapacidad}" '
            f'tipo_discapacidad="{self.tipo_discapacidad}" '
            f'tipo_asignacion="{self.tipo_asignacion}" '
            f'institucion_escolar_id="{self.institucion_escolar_id}" '
            f'grado_actual="{self.grado_actual}" '
            f'tipo_pension="{self.tipo_pension}">')
        
    @classmethod
    def list_jinete_amazona(cls, filters=None, order_by=None, order_direction="asc", page=None, per_page=None):
        """
        Lista los jinetes/amazonas según los filtros y orden especificados.

        :args:

            filters: Diccionario con los filtros a aplicar. Se pueden incluir 'nombre', 'apellido', 'dni' y 'profesionales_asociados'.
            order_by: Campo por el que se ordenará la lista. Puede ser 'nombre' o 'apellido'.
            order_direction: Dirección del ordenamiento. Puede ser 'asc' para ascendente o 'desc' para descendente. Por defecto es 'asc'.
            page: Número de página para la paginación.
            per_page: Cantidad de registros por página.
        
        return: Una tupla con los jinetes/amazonas encontrados, el total de registros, el número de página actual y el total de páginas.
        """
        query = cls.query

        if filters:
            if 'nombre' in filters and filters['nombre']:
                query = query.filter(cls.nombre.ilike(f"%{filters['nombre']}%"))
            if 'apellido' in filters and filters['apellido']:
                query = query.filter(cls.apellido.ilike(f"%{filters['apellido']}%"))
            if 'dni' in filters and filters['dni']:
                query = query.filter(cls.dni.ilike(f"%{filters['dni']}%"))
            if 'profesionales_asociados' in filters and filters['profesionales_asociados']:
                query = query.filter(cls.profesionales_asociados.ilike(f"%{filters['profesionales_asociados']}%"))

        if order_by:
            direction = getattr(db, order_direction.lower(), db.asc)
            if order_by == 'nombre':
                query = query.order_by(direction(cls.nombre))
            elif order_by == 'apellido':
                query = query.order_by(direction(cls.apellido))
                
        
        jinete_amazonas = query.paginate(page=page, per_page=per_page)


        return jinete_amazonas.items, jinete_amazonas.total, jinete_amazonas.page, jinete_amazonas.pages
    
    @classmethod
    def count_jinete_amazonas(cls, filters=None):
        """
        Cuenta la cantidad de jinetes/amazonas aplicando filtros.

        :args:
            filters: Diccionario con filtros opcionales (nombre, apellido, dni, profesionales_asociados).
        
        :return: Cantidad de jinetes/amazonas que cumplen con los filtros.
        """
        query = db.session.query(cls)
        if filters:
            if 'nombre' in filters and filters['nombre']:
                query = query.filter(cls.nombre.ilike(f"%{filters['nombre']}%"))
            if 'apellido' in filters and filters['apellido']:
                query = query.filter(cls.apellido.ilike(f"%{filters['apellido']}%"))
            if 'dni' in filters and filters['dni']:
                query = query.filter(cls.dni.ilike(f"%{filters['dni']}%"))
            if 'profesionales_asociados' in filters and filters['profesionales_asociados']:
                query = query.filter(cls.profesionales_asociados.ilike(f"%{filters['profesionales_asociados']}%"))
        return query.count()

    
    def create_JineteAmazona(cls, nombre, apellido, dni, domicilio, tiene_deuda, becado, telefono, fecha_nacimiento, contacto_emergencia_id, localidad_nacimiento, provincia_nacimiento,
                         profesionales_asociados, certificado_discapacidad, asignacion_familiar,pensionado,propuesta_trabajo,condicion,sede,dias_trabajo,profesor_id, auxiliar_id,conductor_id,caballo_id, situaciones_previsional_id=None,
                         porcentaje_beca=None, diagnostico_discapacidad=None, tipo_discapacidad=None, tipo_asignacion=None, institucion_escolar_id=None, grado_actual = None,
                         tipo_pension = None,):
        """
        Crea un nuevo jinete/amazona en la base de datos.

        :args:
            nombre: Nombre del jinete/amazona.
            apellido: Apellido del jinete/amazona.
            dni: Documento Nacional de Identidad del jinete/amazona.
            domicilio: Domicilio del jinete/amazona.
            tiene_deuda: Indica si el jinete/amazona tiene deudas.
            becado: Indica si el jinete/amazona está becado.
            telefono: Teléfono del jinete/amazona.
            fecha_nacimiento: Fecha de nacimiento del jinete/amazona.
            contacto_emergencia_id: ID del contacto de emergencia.
            localidad_nacimiento: Localidad de nacimiento del jinete/amazona.
            provincia_nacimiento: Provincia de nacimiento del jinete/amazona.
            profesionales_asociados: Profesionales asociados al jinete/amazona.
            certificado_discapacidad: Indica si el jinete/amazona tiene un certificado de discapacidad.
            asignacion_familiar: Indica si el jinete/amazona tiene asignación familiar.
            pensionado: Indica si el jinete/amazona es pensionado.
            propuesta_trabajo: Propuesta de trabajo del jinete/amazona.
            condicion: Condición actual del jinete/amazona.
            sede: Sede del jinete/amazona.
            dias_trabajo: Días de trabajo del jinete/amazona.
            profesor_id: ID del profesor asociado.
            auxiliar_id: ID del auxiliar asociado.
            conductor_id: ID del conductor asociado.
            caballo_id: ID del caballo asociado.
            situaciones_previsional_id: ID de la situación previsional (opcional).
            porcentaje_beca: Porcentaje de la beca (opcional).
            diagnostico_discapacidad: Diagnóstico de discapacidad (opcional).
            tipo_discapacidad: Tipo de discapacidad (opcional).
            tipo_asignacion: Tipo de asignación (opcional).
            institucion_escolar_id: ID de la institución escolar (opcional).
            grado_actual: Grado actual del jinete/amazona (opcional).
            tipo_pension: Tipo de pensión (opcional).
        
        :return: El nuevo jinete/amazona creado.
        
        :raises ValueError: Si el DNI ya se encuentra registrado.
        """
        jinete_amazona1 = JineteAmazona.query.filter_by(dni=dni).first()
        if jinete_amazona1 is None:
            jinete_amazona = cls(  
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                domicilio=domicilio,
                localidad_nacimiento = localidad_nacimiento,
                provincia_nacimiento = provincia_nacimiento,
                tiene_deuda=tiene_deuda,
                becado=becado,
                telefono=telefono,
                fecha_nacimiento=fecha_nacimiento,
                contacto_emergencia_id=contacto_emergencia_id,
                porcentaje_beca=porcentaje_beca,
                profesionales_asociados=profesionales_asociados,
                certificado_discapacidad = certificado_discapacidad,
                diagnostico_discapacidad = diagnostico_discapacidad,
                tipo_discapacidad = tipo_discapacidad,
                asignacion_familiar = asignacion_familiar,
                tipo_asignacion = tipo_asignacion,
                situacion_previsional_id = situaciones_previsional_id,
                institucion_escolar_id = institucion_escolar_id,
                grado_actual = grado_actual,
                pensionado = pensionado,
                tipo_pension = tipo_pension,
                propuesta_trabajo = propuesta_trabajo,
                condicion = condicion,
                sede = sede,
                dias_trabajo = dias_trabajo,
                profesor_id = profesor_id,
                auxiliar_id = auxiliar_id,
                conductor_id = conductor_id,
                caballo_id = caballo_id,
            )
                
            db.session.add(jinete_amazona)
            db.session.commit()
            return jinete_amazona
        raise ValueError("El DNI ya se encuentra registrado")

    @classmethod
    def update_jinete_amazona(cls, id, nombre, apellido, dni, domicilio, tiene_deuda, becado, telefono, fecha_nacimiento, contacto_emergencia_id,localidad_nacimiento, provincia_nacimiento,
                            profesionales_asociados, certificado_discapacidad, asignacion_familiar, pensionado,propuesta_trabajo,condicion,sede,dias_trabajo,profesor_id, auxiliar_id,conductor_id,caballo_id, situacion_previsional_id=None,
                            porcentaje_beca=None, diagnostico_discapacidad=None, tipo_discapacidad=None, tipo_asignacion=None, institucion_escolar_id=None, 
                            grado_actual=None, tipo_pension=None):
        """
        Actualiza la información de un jinete/amazona existente en la base de datos.

        :args:
            id: ID del jinete/amazona a actualizar.
            nombre: Nuevo nombre del jinete/amazona.
            apellido: Nuevo apellido del jinete/amazona.
            dni: Nuevo DNI del jinete/amazona.
            domicilio: Nuevo domicilio del jinete/amazona.
            tiene_deuda: Nuevo estado de deuda del jinete/amazona.
            becado: Nuevo estado de beca del jinete/amazona.
            telefono: Nuevo teléfono del jinete/amazona.
            fecha_nacimiento: Nueva fecha de nacimiento del jinete/amazona.
            contacto_emergencia_id: Nuevo ID del contacto de emergencia.
            localidad_nacimiento: Nueva localidad de nacimiento del jinete/amazona.
            provincia_nacimiento: Nueva provincia de nacimiento del jinete/amazona.
            profesionales_asociados: Nuevos profesionales asociados al jinete/amazona.
            certificado_discapacidad: Nuevo estado del certificado de discapacidad.
            asignacion_familiar: Nuevo estado de asignación familiar.
            pensionado: Nuevo estado de pensionado.
            propuesta_trabajo: Nueva propuesta de trabajo del jinete/amazona.
            condicion: Nueva condición del jinete/amazona.
            sede: Nueva sede del jinete/amazona.
            dias_trabajo: Nuevos días de trabajo del jinete/amazona.
            profesor_id: Nuevo ID del profesor asociado.
            auxiliar_id: Nuevo ID del auxiliar asociado.
            conductor_id: Nuevo ID del conductor asociado.
            caballo_id: Nuevo ID del caballo asociado.
            situaciones_previsional_id: Nuevo ID de la situación previsional (opcional).
            porcentaje_beca: Nuevo porcentaje de la beca (opcional).
            diagnostico_discapacidad: Nuevo diagnóstico de discapacidad (opcional).
            tipo_discapacidad: Nuevo tipo de discapacidad (opcional).
            tipo_asignacion: Nuevo tipo de asignación (opcional).
            institucion_escolar_id: Nuevo ID de la institución escolar (opcional).
            grado_actual: Nuevo grado actual del jinete/amazona (opcional).
            tipo_pension: Nuevo tipo de pensión (opcional).
        
        :return: El jinete/amazona actualizado.
        
        :raises ValueError: Si el DNI ya está en uso por otro jinete/amazona.
        """
        
        # Obtener el jinete/amazona por ID
        jinete_amazona = JineteAmazona.get_jinete_amazona(id)

        if jinete_amazona:
            if dni and dni != jinete_amazona.dni:
                dni_existente = cls.query.filter(cls.dni == dni, cls.id != id).first()
                if dni_existente:
                    raise ValueError("El DNI ya está en uso por otro jinete/amazona.")

            jinete_amazona.nombre = nombre 
            jinete_amazona.apellido = apellido 
            jinete_amazona.dni = dni 
            jinete_amazona.localidad_nacimiento = localidad_nacimiento
            jinete_amazona.provincia_nacimiento = provincia_nacimiento
            jinete_amazona.domicilio = domicilio
            jinete_amazona.tiene_deuda = tiene_deuda 
            jinete_amazona.becado = becado 
            jinete_amazona.telefono = telefono 
            jinete_amazona.fecha_nacimiento = fecha_nacimiento 
            jinete_amazona.contacto_emergencia_id = contacto_emergencia_id 
            jinete_amazona.profesionales_asociados = profesionales_asociados 
            jinete_amazona.certificado_discapacidad = certificado_discapacidad 
            jinete_amazona.asignacion_familiar = asignacion_familiar 
            jinete_amazona.pensionado = pensionado 
            jinete_amazona.localidad_nacimiento = localidad_nacimiento
            jinete_amazona.provincia_nacimiento = provincia_nacimiento

            jinete_amazona.situacion_previsional_id = situacion_previsional_id 
            jinete_amazona.porcentaje_beca = porcentaje_beca 
            jinete_amazona.diagnostico_discapacidad = diagnostico_discapacidad 
            jinete_amazona.tipo_discapacidad = tipo_discapacidad 
            jinete_amazona.tipo_asignacion = tipo_asignacion 
            jinete_amazona.institucion_escolar_id = institucion_escolar_id 
            jinete_amazona.grado_actual = grado_actual 
            jinete_amazona.tipo_pension = tipo_pension 
            jinete_amazona.propuesta_trabajo = propuesta_trabajo 
            jinete_amazona.condicion = condicion 
            jinete_amazona.sede = sede
            jinete_amazona.dias_trabajo = dias_trabajo
            jinete_amazona.profesor_id = profesor_id
            jinete_amazona.auxiliar_id = auxiliar_id
            jinete_amazona.conductor_id = conductor_id
            jinete_amazona.caballo_id = caballo_id


            db.session.commit()
            return jinete_amazona
        return False

    
    @classmethod
    def get_jinete_amazona(cls,id):
        """
        Obtiene un jinete/amazona por su ID.

        :args:
            id: ID del jinete/amazona a obtener.
        
        :return: El jinete/amazona correspondiente al ID, o None si no se encuentra.
        """
        jinete = JineteAmazona.query.filter_by(id=id).first()
        return jinete
    
    def delete_jinete(id):
        """
        Elimina un jinete/amazona de la base de datos.

        :args:
            id: ID del jinete/amazona a eliminar.
        
        :return: True si se elimina correctamente, False en caso contrario.
        
        :raises ValueError: Si no se encuentra el jinete/amazona a eliminar.
        """
        jinete = JineteAmazona.get_jinete_amazona(id)
        if jinete is None:
            ValueError("No se pudo eliminar al jinete/amazona")
        db.session.delete(jinete)
        db.session.commit()
        return True
    
    @classmethod
    def exists_by_dni(cls, dni):
        """
        Verifica si existe un jinete/amazona con el DNI especificado.

        :args:
            dni: Documento Nacional de Identidad a verificar.
        
        :return: True si existe, False en caso contrario.
        """
        return db.session.query(cls).filter_by(dni=dni).first() is not None

    
    @classmethod
    def contar_por_tipo_discapacidad(cls):
        resultados = db.session.query(
        cls.tipo_discapacidad,
        func.count(cls.id).label('cantidad')
        ).filter(cls.tipo_discapacidad.isnot(None)).group_by(cls.tipo_discapacidad).all()

        return {resultado.tipo_discapacidad: resultado.cantidad for resultado in resultados}
    
    @classmethod
    def contar_por_becados(cls):
        return db.session.query(func.count(cls.id)).filter(cls.becado == True).scalar()
    
    @classmethod
    def contar_por_no_becados(cls):
        return db.session.query(func.count(cls.id)).filter(cls.becado == False).scalar()
    
    @classmethod
    def get_jinetes(cls):
        return db.session.query(cls).all()
        
    @classmethod
    def get_deudores(cls):
        return db.session.query(cls).filter(cls.tiene_deuda == True).all()
    
    @classmethod
    def contar_propuesta_trabajo(cls):
        return db.session.query(
        JineteAmazona.propuesta_trabajo,
        func.count(JineteAmazona.id).label("total")
    ).group_by(JineteAmazona.propuesta_trabajo).order_by(func.count(JineteAmazona.id).desc()).all()
        
    @classmethod
    def contar_por_provincia(cls):
        return db.session.query(
        JineteAmazona.provincia_nacimiento,
        func.count(JineteAmazona.id).label("total")
    ).group_by(JineteAmazona.provincia_nacimiento).order_by(func.count(JineteAmazona.id).desc()).all()