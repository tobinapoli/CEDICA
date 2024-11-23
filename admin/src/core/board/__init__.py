from src.core.database import db
from src.core.board.rol import Rol
from src.core.board.rol_permiso import rol_permiso
from src.core.board.permiso import Permiso
from src.core.board.contenido import Contenido
from src.core.board.empleado import Empleado
from src.core.board.pago import Pago
from src.core.board.domicilio import domicilio
from src.core import board
from src.core.board.puesto import Puesto
from src.core.board.contacto_emergencia import contacto_emergencia
from src.core.board.jinete_amazona import JineteAmazona
from src.core.board.ejemplar import ejemplar
from src.core.board.empleado_ejemplar import EmpleadoEjemplar
from src.core.board.tipo_de_jinete import tipo_de_jinete
from src.core.board.ejemplar import tipo_adquisicion
from src.core.board.cobro import cobro as Cobro
from src.core.board.medio_de_pago import MedioDePago

 



def create_permission(**kwargs):
    """
    Crea un nuevo permiso y lo almacena en la base de datos.

    Args:
        **kwargs: Parámetros del permiso.

    Returns:
        Permiso: El permiso creado.
    """
    permission = Permiso(**kwargs)
    db.session.add(permission)
    db.session.commit()
    return permission

def assign_permission_to_role(rol_id, permiso_id):
    """
    Asigna un permiso a un rol en la base de datos.

    Args:
        rol_id (int): ID del rol al que se asignará el permiso.
        permiso_id (int): ID del permiso que se asignará.

    Raises:
        ValueError: Si el rol o permiso no existen.

    Returns:
        new_role_permission: La nueva asignación de rol a permiso.
    """
    role = Rol.query.get(rol_id)
    permission = Permiso.query.get(permiso_id)
    if not role or not permission:
        raise ValueError("El rol o permiso no existe.")
    new_role_permission = rol_permiso.insert().values(rol_id=rol_id, permiso_id=permiso_id)
    db.session.execute(new_role_permission)
    db.session.commit()
    return new_role_permission



def create_jinete_amazona(**kwargs):
    """
    Crea un nuevo jinete amazona y lo almacena en la base de datos.

    Args:
        **kwargs: Parámetros del jinete amazona.

    Returns:
        JineteAmazona: El jinete amazona creado.
    """
    jinete_amazona = board.JineteAmazona(**kwargs)
    db.session.add(jinete_amazona)
    db.session.commit()
    return jinete_amazona

def create_domicilio(**kwargs):
    """
    Crea un nuevo domicilio y lo almacena en la base de datos.

    Args:
        **kwargs: Parámetros del domicilio.

    Returns:
        domicilio: El domicilio creado.
    """
    domicilio = board.domicilio(**kwargs)
    db.session.add(domicilio)
    db.session.commit()
    return domicilio

def create_pago(**kwargs):
    """
    Crea un nuevo pago y lo almacena en la base de datos.

    Args:
        **kwargs: Parámetros del pago.

    Returns:
        Pago: El pago creado.
    """
    pago = board.Pago(**kwargs)
    db.session.add(pago)
    db.session.commit()
    return pago

def create_contacto_emergencia(**kwargs):
    """
    Crea un nuevo contacto de emergencia y lo almacena en la base de datos.

    Args:
        **kwargs: Parámetros del contacto de emergencia.

    Returns:
        contacto_emergencia: El contacto de emergencia creado.
    """
    contacto_emergencia = board.contacto_emergencia(**kwargs)
    db.session.add(contacto_emergencia)
    db.session.commit()
    return contacto_emergencia


def create_ejemplar(**kwargs):
    """
    Crea un nuevo ejemplar y lo almacena en la base de datos.

    Args:
        **kwargs: Parámetros del ejemplar.

    Returns:
        ejemplar: El ejemplar creado.
    """
    ejemplar = board.ejemplar(**kwargs)
    db.session.add(ejemplar)
    db.session.commit()
    return ejemplar

def assign_empleado_to_ejemplar(**kwargs):
    """
    Asigna un empleado a un ejemplar y lo almacena en la base de datos.

    Args:
        **kwargs: Parámetros para la asignación del empleado al ejemplar.

    Returns:
        empleado_ejemplar: La asignación del empleado al ejemplar creada.
    """
    empleado_ejemplar = board.EmpleadoEjemplar(**kwargs)
    db.session.add(empleado_ejemplar)
    db.session.commit()
    return empleado_ejemplar

def create_tipo_de_jinete(**kwargs):
    """
    Crea un nuevo tipo de jinete y lo almacena en la base de datos.

    Args:
        **kwargs: Parámetros del tipo de jinete.

    Returns:
        tipo_de_jinete: El tipo de jinete creado.
    """
    tipo_de_jinete = board.tipo_de_jinete(**kwargs)
    db.session.add(tipo_de_jinete)
    db.session.commit()
    return tipo_de_jinete

def create_tipo_adquisicion(**kwargs):
    """
    Crea un nuevo tipo de adquisición y lo almacena en la base de datos.

    Args:
        **kwargs: Parámetros del tipo de adquisición.

    Returns:
        tipo_adquisicion: El tipo de adquisición creado.
    """
    tipo_adquisicion = board.tipo_adquisicion(**kwargs)
    db.session.add(tipo_adquisicion)
    db.session.commit()
    return tipo_adquisicion

def create_medio_de_pago(**kwargs):
    """
    Crea un nuevo medio de pago y lo almacena en la base de datos.

    Args:
        **kwargs: Parámetros del medio de pago.

    Returns:
        medio_de_pago: El medio de pago creado.
    """
    medio_de_pago = board.MedioDePago(**kwargs)
    db.session.add(medio_de_pago)
    db.session.commit()
    return medio_de_pago

