from datetime import datetime
from flask import Blueprint, flash, redirect, session,url_for
from flask import render_template
from src.web.handlers.error import error_403
from src.core import board
from src.core.board import Cobro
from src.web.handlers.auth import login_required
from src.web.handlers.auth import check_permission
from flask import request
from src.core.board import JineteAmazona
from src.core.board import Empleado
from src.core.board import MedioDePago
from os import environ


bp = Blueprint('cobro', __name__, url_prefix='/cobros')

@bp.route('/<int:jinete_id>')  
@login_required
@check_permission('index_cobro')
def index(jinete_id):
    
    """
    Muestra el índice de cobros para un jinete específico, accesible solo para usuarios con el permiso index_cobro.

    Parámetros:
    -----------
    - jinete_id (int): ID del jinete cuyos cobros se muestran.

    Filtros de búsqueda y ordenación (opcional):
    -------------------------------------------
    - fechaMin y fechaMax (str): Rango de fechas para filtrar.
    - medio_de_pago (str): Filtro por método de pago.
    - empleado.nombre y empleado.apellido (str): Filtrar por nombre o apellido del empleado.
    - ordenar_por (str): Campo de ordenación (predeterminado es "fecha").
    - orden (str): Dirección de ordenación ("asc" o "desc").

    Retorna:
    --------
    Render de la plantilla 'cobros/index.html' con los cobros paginados, filtrados, y ordenados,
    junto con la información de paginación y filtros.
    """
    
    if not check_permission('index_cobro'):
        return error_403("No tienes permisos para acceder a este recurso")
    if(board.Cobro.existe_jinete(jinete_id) == False):
        return redirect(url_for('jinete_amazona.index'))
    filters = {
        'fechaMin': request.args.get('fechaMin', ''),  
        'fechaMax': request.args.get('fechaMax', ''),  
        'medio_de_pago': request.args.get('medio_de_pago', ''),   
        'empleado.nombre': request.args.get('empleado.nombre', ''),
        'empleado.apellido': request.args.get('empleado.apellido', ''),  
    }

    current_date = datetime.now().strftime('%Y-%m-%d')
    
    
    page = request.args.get('page', 1, type=int)  
    per_page = int(environ.get('PAGINATION_PER_PAGE', 25))

    order_by = request.args.get('ordenar_por', 'fecha')  
    order_direction = request.args.get('orden', 'asc')  
    
    medios_de_pago = MedioDePago.get_medios_de_pago()

    cobros = board.Cobro.get_cobros_filtro(filters=filters, order_by=order_by, order_direction=order_direction, page=page, per_page=per_page, jinete_id=jinete_id)
    
    total_pages = cobros.pages
    
    start = max(1, page - 2)
    end = min(total_pages, page + 2)
    
    return render_template('cobros/index.html', cobros=cobros, jinete_id=jinete_id, medio_de_pago=medios_de_pago, current_date=current_date,page=page, total_pages = total_pages, start=start, end=end)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@check_permission('create_cobro')
def create():
    """
    Muestra el formulario para crear un nuevo cobro. Verifica permisos y valida los datos ingresados.

    Si el método es GET, se cargan los datos necesarios para llenar el formulario: jinetes, empleados y medios de pago.
    Si es POST, se procesan los datos del formulario, verificando que sean válidos. Cualquier error se almacena en 
    la sesión y redirige al formulario con los mensajes de error.

    Validaciones de datos:
    ----------------------
    - Monto: Validación de tipo numérico.
    - Fecha: Validación de formato.
    - Empleado y jinete: Verificación de existencia en la base de datos.

    Parámetros del formulario (POST):
    ---------------------------------
    - monto (float): Monto del cobro.
    - fecha (str): Fecha del cobro.
    - medio_de_pago (int): ID del medio de pago.
    - jinetes (int): ID del jinete.
    - empleado_id (int): ID del empleado.
    - observaciones (str): Observaciones adicionales.
    - continuar (str): Si es "1", redirige al formulario de creación en blanco tras enviar.

    Retorna:
    --------
    - Render de 'cobros/create.html' en GET.
    - Redirige a la creación en blanco o al índice de cobros en caso de éxito.
    """
    
    if not check_permission('create_cobro'):
        return error_403("No tienes permisos para acceder a este recurso")
    jinetes_amazonas = JineteAmazona.get_jinetes()
    empleados = Empleado.get_all_empleado()
    medios_de_pago = MedioDePago.get_medios_de_pago()
    errors = {}
    
    if 'error_monto' in session:
        errors['monto'] = session.pop('error_monto')  
    if 'error_fecha' in session:
        errors['fecha'] = session.pop('error_fecha')  

    current_date = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        monto = request.form.get('monto')
        fecha = request.form.get('fecha')
        medio_de_pago = request.form.get('medio_de_pago')
        jinetes = request.form.get('jinetes')
        empleado_id = request.form.get('empleado_id')
        observaciones = request.form.get('observaciones')
        continuar = request.form.get('continuar') 
        
        try:
            validar_monto(float(monto)) 
            validar_fecha(fecha) 
            existe_empleado(empleado_id) 
            existe_jinete(jinetes) 
        except ValueError as e:
            if 'monto' in str(e):
                session['error_monto'] = str(e)
            elif 'fecha' in str(e):
                session['error_fecha'] = str(e)  

            return redirect(url_for('cobro.create'))
            

        cobro = board.Cobro.create_cobro(
            jinetes=jinetes,
            monto=monto,
            fecha=fecha,
            medio_de_pago=medio_de_pago,
            empleado_id=empleado_id,
            observaciones=observaciones
        )
        flash("Cobro creado con éxito", "success")
        if continuar.__eq__("1"):
            return redirect(url_for('cobro.create'))
        else:
            return redirect(url_for('cobro.index', jinete_id=jinetes))

    return render_template('cobros/create.html', form_data={}, jinetes=jinetes_amazonas, empleados=empleados, errors=errors, current_date=current_date, medio_de_pago=medios_de_pago)





@bp.route('/<int:jinete_id>/<int:cobro_id>/edit', methods=['GET', 'POST'])
@check_permission('edit_cobro')
def update_cobro(jinete_id,cobro_id):
    """
    Muestra el formulario de edición de un cobro específico y maneja la actualización de sus datos.

    Validaciones:
    - Verifica permisos de edición de cobro.
    - Si el cobro no existe, redirige al índice de cobros del jinete.

    Si el método es GET, se obtienen los datos del cobro, lista de jinetes, empleados, y medios de pago para el formulario.
    Si es POST, realiza las siguientes validaciones antes de actualizar:
    - Monto: Valida que sea numérico.
    - Fecha: Verifica el formato de la fecha.
    - Empleado y jinete: Verifica que ambos existan en la base de datos.

    Parámetros del formulario (POST):
    ---------------------------------
    - monto (float): Monto del cobro.
    - fecha (str): Fecha del cobro.
    - medio_de_pago (int): ID del medio de pago.
    - empleado_id (int): ID del empleado asociado al cobro.
    - observaciones (str): Observaciones adicionales.

    Retorna:
    --------
    - Render de 'cobros/update.html' en GET.
    - Redirige al índice de cobros si la actualización es exitosa.
    """
    
    if not check_permission('edit_cobro'):
        return error_403("No tienes permisos para acceder a este recurso")
    cobro = Cobro.get_cobro(cobro_id)
    jinetes_amazonas = JineteAmazona.get_jinetes()
    empleados = Empleado.get_all_empleado()
    medios_de_pago = MedioDePago.get_medios_de_pago()

    if not cobro:
         return redirect(url_for('cobro.index', jinete_id=jinete_id))
    

    errors = {}
    
    if 'error_monto' in session:
        errors['monto'] = session.pop('error_monto')  
    if 'error_fecha' in session:
        errors['fecha'] = session.pop('error_fecha')  
    
    current_date = datetime.now().strftime('%Y-%m-%d')

    form_data = {
        'fecha': cobro.fecha.strftime('%Y-%m-%d') if cobro.fecha else '',
        'monto': cobro.monto,
        'medio_de_pago': cobro.medio_de_pago,
        'empleado_id': cobro.empleado_id,
        'observaciones': cobro.observaciones,
    }
    if request.method == 'POST':
        monto = request.form.get('monto')
        fecha = request.form.get('fecha')
        medio_de_pago = request.form.get('medio_de_pago')
        empleado_id = request.form.get('empleado_id')
        observaciones = request.form.get('observaciones')
        try:
            validar_monto(float(monto))  
            validar_fecha(fecha)  
            existe_empleado(empleado_id) 
            existe_jinete(jinete_id) 
        except ValueError as e:
            if 'monto' in str(e):
                session['error_monto'] = str(e)
            elif 'fecha' in str(e):
                session['error_fecha'] = str(e)  
            return redirect(url_for('cobro.update_cobro', jinete_id=jinete_id, cobro_id=cobro_id))
        cobro = Cobro.update_cobro(cobro_id,
            monto=monto,
            fecha=fecha,
            medio_de_pago=medio_de_pago,
            empleado_id=empleado_id,
            observaciones=observaciones
        )
        flash("Cobro actualizado con éxito", "success")
        return redirect(url_for('cobro.index', jinete_id=jinete_id))
    return render_template('cobros/update.html', cobro=cobro, form_data=form_data,empleados=empleados, errors=errors,jinetes=jinetes_amazonas, jinete_id=jinete_id, medio_de_pago=medios_de_pago, current_date=current_date)

@bp.route('/<int:jinete_id>/<int:cobro_id>/show') 
@login_required
@check_permission('view_cobro')
def show(jinete_id,cobro_id):
    """
    Muestra los detalles de un cobro específico.

    Requiere permiso 'view_cobro' para acceder a los datos de cobro.
    Si el permiso no se concede, devuelve un error 403.

    Parámetros:
    ----------
    - jinete_id (int): ID del jinete asociado al cobro.
    - cobro_id (int): ID del cobro a mostrar.

    Retorna:
    --------
    - Render de 'cobros/show.html' con los detalles del cobro, empleado y medio de pago.
    """
    if not check_permission('view_cobro'):
        return error_403("No tienes permisos para acceder a este recurso")
    cobro = Cobro.get_cobro(cobro_id)
    empleado = Cobro.obtener_empleado(cobro.empleado_id)
    medio_de_pago = Cobro.obtener_medio_pago(cobro.medio_de_pago)
    return render_template('cobros/show.html', jinete_id=jinete_id, cobro=cobro, empleado=empleado, medio_de_pago=medio_de_pago)

@bp.route('/<int:jinete_id>/<int:cobro_id>/delete', methods=['POST']) 
@login_required
@check_permission('delete_cobro')
def delete(jinete_id, cobro_id):
    cobro = Cobro.get_cobro(cobro_id)
    if not cobro:
        flash("Cobro no encontrado", "error")
        return redirect(url_for('cobro.index', jinete_id=jinete_id))

    Cobro.delete_cobro(cobro_id)
    flash("Cobro eliminado con éxito", "success")
    return redirect(url_for('cobro.index', jinete_id=jinete_id))




def existe_empleado(empleado_id):
    """
    Verifica que el ID del empleado no sea nulo.

    Parámetros:
    ----------
    - empleado_id (int): ID del empleado a verificar.

    Excepciones:
    -----------
    - ValueError: Si el empleado_id es None.
    """
    if empleado_id is None:
        raise ValueError("El empleado no puede ser nulo")
    
    
def existe_jinete(jinete_id):
    """
    Verifica que el ID del jinete no sea nulo.

    Parámetros:
    ----------
    - jinete_id (int): ID del jinete a verificar.

    Excepciones:
    -----------
    - ValueError: Si el jinete_id es None.
    """
    if jinete_id is None:
        raise ValueError("El jinete no puede ser nulo")

def validar_monto(monto):
    """
    Valida que el monto sea positivo y no igual a cero.

    Parámetros:
    ----------
    - monto (float): Monto a validar.

    Excepciones:
    -----------
    - ValueError: Si el monto es negativo o cero.

    Retorna:
    --------
    - True si el monto es válido.
    """
    if monto < 0:
        raise ValueError("El monto no puede ser negativo")
    if monto == 0:
        raise ValueError("El monto no puede ser cero")
    return True

def validar_fecha(fecha_str):
    """
    Valida el formato y el rango de la fecha proporcionada.

    Parámetros:
    ----------
    - fecha_str (str): Fecha en formato 'YYYY-MM-DD'.

    Excepciones:
    -----------
    - ValueError: Si el formato de fecha es inválido, la fecha es mayor que la actual o menor al 1 de enero de 1994.

    Retorna:
    --------
    - True si la fecha es válida.
    """
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d') 
    except ValueError:
        raise ValueError("Formato de fecha inválido")
    
    if fecha > datetime.now():
        raise ValueError("La fecha no puede ser mayor a la actual")
    
    fecha_minima = datetime(1994, 1, 1)
    if fecha < fecha_minima:
        raise ValueError("La fecha no puede ser menor al 1 de enero de 1994")
    
    return True