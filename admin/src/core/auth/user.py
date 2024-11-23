from copy import deepcopy
from datetime import datetime
import bcrypt
from src.core.database import db
from src.core.board.empleado import Empleado
from src.core.board.rol import Rol 


class User(db.Model):
    __tablename__ = 'user'  

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False, index=True)
    alias = db.Column(db.String(50), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    registroAprobado = db.Column(db.Boolean, default=True)
    avatar =  db.Column(db.String(255), nullable=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=True,) 
    password = db.Column(db.String(255), nullable=True)
    esUsuarioGoogle = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    role = db.relationship('Rol', back_populates='users', lazy = 'joined') 

    def __repr__(self):
        return f'<User #{self.id} nombre="{self.alias} email="{self.email}>'
    
    @classmethod
    def get_user(cls,user_id): 
        user = User.query.get_or_404(user_id)
        return deepcopy(user)

    @classmethod
    def create_user(cls, email, alias, password=None, rol_id=None, registroAprobado=True, esUsuarioGoogle=False): 
        user1 = cls.get_by_email(email)
        if user1 is None:
            hashed_password = None
            if password:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = cls(email=email, alias=alias, password=hashed_password, rol_id=rol_id, registroAprobado=registroAprobado, esUsuarioGoogle=esUsuarioGoogle) 
            db.session.add(user)
            db.session.commit()
            return user
        raise ValueError("El correo electrónico ya está registrado")
    
    def register_google_user(id_info):
        """
        Registra un usuario autenticado con Google si no existe en la base de datos.

        Parámetros:
        -----------
        - id_info (dict): Información devuelta por Google (email, nombre, etc.).

        Retorna:
        --------
        - User: El usuario registrado o existente.
        """
        email = id_info.get('email')
        alias = id_info.get('name')  # Cambiar si usás otro atributo para alias
        user1 = User.get_by_email(email)
        if user1 is None:
            user = User.create_user(email=email, alias=alias, registroAprobado=False, esUsuarioGoogle=True)
            return user
        
        raise ValueError("El correo electrónico ya está registrado")

    
    
    @classmethod
    def update_user(self, id, data):
        user = User.query.get(id)
        if user is not None:
            if data.get("new_email") and data.get("new_email") != user.email:
                email_existente = User.query.filter(User.email == data.get("new_email"), User.id != id).first()
                if email_existente:
                    raise ValueError("El correo electrónico ya está en uso por otro usuario.")

            user.email = data.get("new_email", user.email)
            user.alias = data.get("alias", user.alias)

            new_password = data.get("password")
            if new_password:
                user.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


            user.rol_id = data.get("rol_id", user.rol_id)


            if "activo" in data:  
                user.activo = data.get("activo") == True if isinstance(data.get("activo"), bool) else data.get("activo") == "True"
            
            if "registroAprobado" in data:
                user.registroAprobado = data.get("registroAprobado") == True if isinstance(data.get("registroAprobado"), bool) else data.get("registroAprobado") == "True"

            db.session.commit()
        return None

    
    @classmethod
    def get_all_users(self, page=None, per_page=None, filters=None, order_by='id', order_dir='asc'):
        query = self.query

        if filters:
            if 'email' in filters and filters['email']:
                query = query.filter(self.email.ilike(f"%{filters['email']}%"))
            if 'activo' in filters and filters['activo']:
                query = query.filter(self.activo == (filters['activo'] == 'True'))
            if 'rol' in filters and filters['rol']:
                query = query.join(Rol).filter(Rol.nombre == filters['rol'])

        if order_by:
            direction = getattr(db, order_dir.lower(), db.asc)
            if order_by == 'email':
                query = query.order_by(direction(self.email))
            elif order_by == 'created_at':
                query = query.order_by(direction(self.created_at))
                
        if page and per_page:
            users = query.paginate(page=page, per_page=per_page, error_out=False)
        else:
            users = query.all()
            
        return users
    
    
    @classmethod
    def count_users(cls, filters=None):
        query = cls.query
        if filters:
            if 'email' in filters and filters['email']:
                query = query.filter(cls.email.ilike(f"%{filters['email']}%"))
            if 'activo' in filters and filters['activo']:
                query = query.filter(cls.activo == (filters['activo'] == 'True'))
            if 'rol' in filters and filters['rol']:
                query = query.join(Rol).filter(Rol.nombre == filters['rol'])
        return query.count()

    def assign_role(self, rol_id):
        new_role = Rol.get_by_id(rol_id) 
        if new_role:
            self.role = new_role
            db.session.commit()
            return True
        return False

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    

    def delete_user(self):
        if self is None:
            ValueError("No se pudo eliminar el usuario")
        db.session.delete(self)
        db.session.commit()
        return True 
    
    def get_permission(self):
        if self.role:
            return [permiso.nombre for permiso in self.role.permisos]
        return []
    
    def get_users_without_empleado():
        # Buscar los usuarios que no tienen un empleado asignado
        users_without_empleado = User.query.outerjoin(Empleado, Empleado.user_id == User.id) \
                                        .filter(Empleado.user_id == None).all()
        return users_without_empleado
    
    def aceptar_registro(self):
        if not self.registroAprobado:
            self.registroAprobado = True
            db.session.commit()
    