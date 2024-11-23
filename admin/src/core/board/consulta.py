from datetime import datetime
from src.core.database import db
from sqlalchemy import desc, asc

class Consulta(db.Model):
    """Modelo que representa una consulta en el módulo de contacto."""
    id = db.Column(db.Integer, primary_key=True)
    nombrecompleto = db.Column(db.String(200), nullable=False)
    correo = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), default="pendiente", nullable=False)
    comentario_interno = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    closed_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """Devuelve una representación en cadena de la consulta."""
        return f'<Consulta #{self.id} de {self.nombrecompleto}>'

    @classmethod
    def create(cls, **kwargs):
        consulta = cls(**kwargs)
        db.session.add(consulta)
        db.session.commit()
        return consulta
    
    @classmethod
    def list_consultas(cls, page, per_page, filters=None, sort_by='created_at', order='asc'):
        """Lista las consultas, aplicando filtros y paginación."""
        query = Consulta.query

        # Filtrado
        if filters:
            if 'nombrecompleto' in filters and filters['nombrecompleto']:
                query = query.filter(Consulta.nombrecompleto.ilike(f"%{filters['nombrecompleto']}%"))
            if 'correo' in filters and filters['correo']:
                query = query.filter(Consulta.correo.ilike(f"%{filters['correo']}%"))
            if 'estado' in filters and filters['estado']:
                query = query.filter(Consulta.estado.ilike(f"%{filters['estado']}%"))

        # Ordenación
        sort_column = getattr(Consulta, sort_by, None)
        if sort_column is None:
            raise ValueError(f"Columna de orden inválida: {sort_by}")

        if order == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # Paginación
        return query.paginate(page=page, per_page=per_page)

    @classmethod
    def create_consulta(cls, nombrecompleto, correo, mensaje):
        """Crea una nueva consulta en la base de datos."""
        consulta = cls(
            nombrecompleto=nombrecompleto,
            correo=correo,
            mensaje=mensaje,
            estado="created"
        )
        db.session.add(consulta)
        db.session.commit()
        return consulta

    @classmethod
    def update_consulta(cls, id, estado, comentario_interno=None):
        """Actualiza el estado de una consulta y añade un comentario interno."""
        consulta = cls.query.get(id)
        consulta.estado = estado
        consulta.comentario_interno = comentario_interno
        db.session.commit()

    @classmethod
    def get_consulta(cls, id):
        """Obtiene una consulta por su identificador."""
        return cls.query.get(id)

    @classmethod
    def delete_consulta(cls, id):
        """Elimina una consulta por su identificador."""
        consulta = cls.query.get(id)
        if consulta:
            db.session.delete(consulta)
            db.session.commit()
        else:
            raise ValueError("Consulta no encontrada")