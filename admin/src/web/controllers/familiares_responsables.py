from threading import local
from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.web.handlers.auth import check_permission, login_required
from src.core.board import domicilio
from src.core.board.familiares_responsables import FamiliarResponsable, TipoEscolaridad
from src.core.board.jinete_amazona import JineteAmazona
from src.core.database import db
from src.web.controllers.form.familiares_form import FamiliarForm
from src.core.board.domicilio import TipoProvincia
from src.web.handlers.auth import check_permission, login_required

bp = Blueprint('familiares_responsables', __name__)




@login_required
@check_permission("create_familiares")
@bp.route('/familiares/create/<int:jinete_id>', methods=['GET', 'POST'])
def create(jinete_id):

    """Crea un nuevo familiar responsable para un jinete específico."""
    form = FamiliarForm()

    if form.validate_on_submit():
        try:
            # Accede a los datos del formulario a través del objeto form
            parentesco = form.parentesco.data
            nombre = form.nombre.data
            apellido = form.apellido.data
            dni = form.dni.data
            celular = form.celular.data
            email = form.email.data
            nivel_escolaridad = form.nivel_escolaridad.data
            actividad_ocupacion = form.ocupacion.data
            # Accede a los datos del formulario a través del objeto form
            parentesco = form.parentesco.data
            nombre = form.nombre.data
            apellido = form.apellido.data
            dni = form.dni.data
            celular = form.celular.data
            email = form.email.data
            nivel_escolaridad = form.nivel_escolaridad.data
            actividad_ocupacion = form.ocupacion.data
            
            calle = form.calle.data
            numero = form.numero.data
            depto = form.depto.data
            localidad = form.localidad.data
            provincia_familiar = form.provincia.data

            # Lógica para crear el domicilio y el familiar responsable
            calle = form.calle.data
            numero = form.numero.data
            depto = form.depto.data
            localidad = form.localidad.data
            provincia_familiar = form.provincia.data

            # Lógica para crear el domicilio y el familiar responsable
            domicilio_nuevo = domicilio.create_domicilio(
                domicilio,
                calle=calle,
                numero=numero,
                depto=depto,
                localidad=localidad,
                provincia=provincia_familiar,
            )

            FamiliarResponsable.create_familiar_responsable(
                parentesco, nombre, apellido, dni, domicilio_nuevo.id, celular, email, nivel_escolaridad, actividad_ocupacion, jinete_id
            )
            flash('Familiar responsable creado exitosamente.', 'success')
            return redirect(url_for('jinete_amazona.index'))
        except ValueError as e:
            flash(str(e), 'danger')

    
    return render_template('familiares_responsables/create.html.jinja', form=form, jinete_id=jinete_id, nivel_escolaridad = TipoEscolaridad, provincia = TipoProvincia)

    
@bp.route('/familiares/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@check_permission("update_familiares")
def update(id):
    """Actualiza la información de un familiar responsable existente.

    Args:
        id (int): ID del familiar responsable a actualizar.

    Returns:
        Renderiza la plantilla para actualizar el familiar o redirige al índice de jinetes al éxito.
    """
    familiar = FamiliarResponsable.get_familiar(id)
    domicilio_familiar = domicilio.get_domicilio(familiar.domicilio)

    
    form = FamiliarForm(obj=familiar)

    if request.method == 'POST' and form.validate_on_submit():
        tipo_parentesco = form.parentesco.data
        nombre_familiar = form.nombre.data
        apellido_familiar = form.apellido.data
        DNI_familiar = form.dni.data
        celular = form.celular.data
        ocupacion_familiar = form.actividad_ocupacion.data
        email = form.email.data
        nivel_escolaridad = form.nivel_escolaridad.data
        
        
        calle_familiar = form.calle.data
        numero_familiar = form.numero.data
        depto_familiar = form.depto.data
        localidad_familiar = form.localidad.data
        provincia_familiar = form.provincia.data
        calle_familiar = form.calle.data
        numero_familiar = form.numero.data
        depto_familiar = form.depto.data
        localidad_familiar = form.localidad.data
        provincia_familiar = form.provincia.data
        domicilio.update_domicilio(
            id = id,
            calle = calle_familiar,
            numero = numero_familiar,
            depto = depto_familiar,
            localidad = localidad_familiar,
            provincia = provincia_familiar,
        )
        
        FamiliarResponsable.update(
            id = familiar.id,
            parentesco=tipo_parentesco,
            nombre=nombre_familiar,
            apellido=apellido_familiar,
            dni=DNI_familiar,
            celular=celular,
            email=email,
            nivel_escolaridad=nivel_escolaridad,
            actividad_ocupacion=ocupacion_familiar,
            domicilio_id=id
        )

        flash('Familiar actualizado exitosamente', 'success')
        return redirect(url_for('jinete_amazona.index'))  

    
    return render_template('familiares_responsables/update.html.jinja', form_data={},familiar_responsable=familiar,direccion_domicilio=domicilio_familiar, nivel_escolaridad=TipoEscolaridad,form=form)
       
@bp.route('/familiares/delete/<int:id>', methods=['GET','POST'])
@login_required
@check_permission("delete_familiares")
def delete(id):
    """Elimina un familiar responsable por su ID.

    Args:
        id (int): ID del familiar responsable a eliminar.

    Returns:
        Redirige al índice de jinetes después de eliminar.
    """
    FamiliarResponsable.delete_familiar(id)
    flash('Familiar responsable eliminado exitosamente.', 'success')
    return redirect(url_for('jinete_amazona.index'))

@bp.route('/familiares/show/<int:id>', methods=['GET'])

def show(id):
    """Muestra los detalles de un familiar responsable específico.

    Args:
        id (int): ID del familiar responsable a mostrar.

    Returns:
        Renderiza la plantilla que muestra los detalles del familiar y su domicilio.
    """
    familiar = FamiliarResponsable.get_familiar(id)  
    domicilio_show = domicilio.get_domicilio(familiar.domicilio) 

    return render_template(
        'familiares_responsables/show.html.jinja', 
        familiar=familiar,
        domicilio=domicilio_show
    )
    
