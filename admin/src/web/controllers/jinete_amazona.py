from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from src.core.board.domicilio import TipoProvincia
from src.core.board import ejemplar
from src.core.board.empleado import Empleado
from src.core.board.familiares_responsables import FamiliarResponsable, TipoEscolaridad
from src.core.board.institucion_escolar import InstitucionEscolar
from src.core.board.situacion_previsional import SituacionPrevisional
from src.web.handlers.auth import check_permission, login_required
from src.web.controllers.form.jinete_amazona_form import JineteAmazonaForm
from src.core.board.documento import Documento, TipoDocumento, TipoTitular
from src.web.controllers import documento as documento_controller
from src.core.board.jinete_amazona import  JineteAmazona, TipoAsignacion, TipoCondicion, TipoDiscapacidad, TipoPension, TipoPropuesta, TipoSede
from src.core import board
from os import environ



bp = Blueprint("jinete_amazona", __name__, url_prefix="/jinete_amazona")
@bp.route("/", methods=["GET"])
@login_required
@check_permission("index_jinete")
def index():
    """
    Renderiza la página de índice mostrando jinetes y sus documentos asociados.

    Esta función maneja la paginación tanto para jinetes como para documentos, 
    aplica filtros según la entrada del usuario y recupera datos relevantes para su visualización.

    Parámetros de consulta:
        - page (int): El número de página para los jinetes (por defecto es 1).
        - page2 (int): El número de página para los documentos (por defecto es 1).
        - section (str): La sección a mostrar (por defecto es 'jinetes').
        - nombre (str): Filtra por el nombre del jinete.
        - apellido (str): Filtra por el apellido del jinete.
        - dni (str): Filtra por el DNI del jinete.
        - profesionales_asociados (str): Filtra por profesionales asociados.
        - titulo (str): Filtra por el título del documento.
        - tipo_documento (str): Filtra por tipo de documento.
        - ordenar_por (str): El campo por el que se ordenan los jinetes (por defecto es 'nombre').
        - orden (str): La dirección de ordenamiento para jinetes (por defecto es 'asc').
        - order_by2 (str): El campo por el que se ordenan los documentos (por defecto es 'fecha_subida').
        - order_direction2 (str): La dirección de ordenamiento para documentos (por defecto es 'asc').

    Retorna:
        - render_template: Renderiza la plantilla de índice con los datos de jinetes y documentos filtrados, 
                          paginados y ordenados.
    """
    jinetes_pages = request.args.get('page', 1, type=int)
    documentos_pages = request.args.get('page2', 1, type=int)
    section = request.args.get('section', 'jinetes')
    filters = {
        'nombre': request.args.get('nombre', ''),
        'apellido': request.args.get('apellido', ''),
        'dni': request.args.get('dni', ''),
        'profesionales_asociados': request.args.get('profesionales_asociados', ''),
    }
    
    docs_filters = {
        'titulo': request.args.get('titulo', ''),
        'tipo_documento': request.args.get('tipo_documento', '')
    }

    per_page = int(environ.get('PAGINATION_PER_PAGE', 25))

    order_by = request.args.get('ordenar_por', 'nombre')
    order_direction = request.args.get('orden', 'asc')
    
    order_by2 = request.args.get('order_by2', 'fecha_subida')
    order_direction2 = request.args.get('order_direction2', 'asc')
    
    documentos,total2,current_page2, total_pages2 = Documento.get_filtered_documentos(docs_filters, order_by2, order_direction2,page = documentos_pages, per_page = per_page, tipo_titular = TipoTitular.jya)
    documentos_con_jinete = []
    for documento in documentos:
        jinete = None
        if documento.tipo_titular == TipoTitular.jya:
            if documento.jinete_id:
                jinete = board.JineteAmazona.get_jinete_amazona(documento.jinete_id)
                documentos_con_jinete.append({
                    'documento': documento,
                    'jinetes': jinete,
                     
             })
                
    jinetes_amazonas,total,current_page,total_pages = board.JineteAmazona.list_jinete_amazona(filters=filters, order_by=order_by, order_direction=order_direction,page=jinetes_pages, per_page=per_page)
    
    tipos_docs = TipoDocumento.get_tipo_doc_jinetes()
    start = max(1, jinetes_pages - 2)
    end = min(total_pages, jinetes_pages + 2)
    
    start2 = max(1, documentos_pages - 2)
    end2 = min(total_pages2, documentos_pages + 2)
    
    return render_template("jinete_amazona/index.html.jinja",current_page2 = current_page2, total=total,
                           total_pages2=total_pages2, total2 = total2,
                           jinetes_amazonas=jinetes_amazonas, filters=filters, 
                           order_by=order_by, order_direction=order_direction,
                           section=section, tipos_docs=tipos_docs, documentos=documentos_con_jinete,
                           page=jinetes_pages, per_page=per_page,start=start,end=end,total_pages=total_pages,
                           page2 = documentos_pages, start2=start2,end2=end2, current_page=current_page)


@bp.route("/create", methods=["GET", "POST"])
@login_required
@check_permission("create_jinete")
def create():
    """
    Maneja la creación de un nuevo jinete/amazona.

    Esta función procesa la solicitud POST para crear un nuevo jinete/amazona, 
    guarda los datos del formulario y gestiona la creación de registros relacionados.

    Retorna:
        - render_template: Renderiza el formulario de creación si la solicitud es GET.
        - redirección: Redirige a la página de índice si se crea el jinete con éxito.
    """
    
    form = JineteAmazonaForm()
    empleado = Empleado.get_empleado_activos()
    caballos = ejemplar.get_all_ejemplar()
    

    
    if request.method == "POST":
       
        if form.validate_on_submit():
            nombre = form.nombre.data  
            apellidos = form.apellido.data
            dni = form.dni.data
            telefono = form.telefono.data
            porcentaje_beca = form.porcentaje_beca.data
            profesionales_asociados = form.profesionales_asociados.data
            diagnostico_discapacidad = form.diagnostico_discapacidad.data
            diagnostico_otro= form.diagnostico_otro.data
            localidad_nacimiento = form.localidad_nacimiento.data
            provincia_nacimiento = form.provincia_nacimiento.data
            grado_actual = form.grado_actual.data
            tipo_discapacidad = form.tipo_discapacidad.data
            tipo_asignacion = form.tipo_asignacion.data
            tipo_pension = form.tipo_pension.data
            
            becado_value = form.becado.data
            becado = True if becado_value == 'True' else False
            
            tiene_deuda_value = form.tiene_deuda.data
            tiene_deuda = True if tiene_deuda_value == 'True' else False
            
            certificado_discapacidad_value = form.certificado_discapacidad.data
            certificado_discapacidad = True if certificado_discapacidad_value == 'True' else False
            
            asignacion_familiar_value = form.asignacion_familiar.data
            asignacion_familiar = True if asignacion_familiar_value == 'True' else False
            
            pensionado_value = form.pensionado.data
            pensionado = True if pensionado_value == 'True' else False
            
            #Situacion Previsional
            obra_social = form.obra_social.data
            numero_afiliado=form.numero_afiliado.data
            observaciones = form.observaciones.data
            posee_curatela_value = form.posee_curatela.data
            posee_curatela = True if posee_curatela_value == 'True' else False
            
            #Domicilio del jinete
            
            calle = form.calle.data
            numero = form.numero.data
            depto = form.depto.data
            localidad = form.localidad.data
            provincia = form.provincia.data
            
            #Contacto de emergencia
            
            contacto_telefono = form.contacto_telefono.data
            contacto_nombre = form.contacto_nombre.data
            
            #Instiucion Escolar
            nombre_institucion = form.nombre_institucion.data
            direccion_institucion = form.direccion_institucion.data
            telefono_institucion = form.telefono_institucion.data
            observaciones_institucion = form.observaciones_institucion.data
            fecha_nacimiento = form.fecha_nacimiento.data
            
            
            
            # Trabajo en la institucion
            propuesta_trabajo = form.propuesta_trabajo.data
            condicion = form.condicion.data
            sede = form.sede.data
            dias_trabajo = form.dias_trabajo.data
            profesor_id = request.form.get("profesor_id")
            auxiliar_id = request.form.get("auxiliar_id")
            conductor_id = request.form.get("conductor_id")
            caballo_id = request.form.get("caballo_id")

            
            tipos_documento = request.form.getlist('tipo_documento[]')
            tipos_entrada = request.form.getlist('documento_tipo[]')
            archivos = request.files.getlist('documentos[]')
            enlaces = request.form.getlist('links[]')
            
            
            if JineteAmazona.exists_by_dni(dni):
                flash("El DNI ya está registrado.", "error")
                return redirect(url_for("jinete_amazona.create"))

            if diagnostico_discapacidad == 'OTRO' and not diagnostico_otro:
                flash("Debe especificar el diagnóstico si selecciona 'OTRO'", 'error')
                return redirect(url_for('formulario_diagnostico'))
            diagnostico_final = diagnostico_otro if diagnostico_discapacidad == 'OTRO' else diagnostico_discapacidad
        
            
            try:
                
                contacto = board.contacto_emergencia.create_contacto_emergencia(board.contacto_emergencia, 
                    nombre=contacto_nombre, telefono=contacto_telefono
                ) 

                

                nuevo_domicilio = board.domicilio.create_domicilio(board.domicilio,
                    calle=calle,
                    numero=numero,
                    depto=depto,
                    localidad=localidad,
                    provincia=provincia
                )
                
                
                
                nueva_situacionPrevisional = SituacionPrevisional.create_situacion_previsional(
                    obra_social = obra_social,
                    numero_afiliado = numero_afiliado,
                    posee_curatela = bool(posee_curatela),
                    observaciones = observaciones)
                
               
        
               

                nueva_institucion = InstitucionEscolar.create_institucion_escolar(
                    nombre=nombre_institucion,
                    direccion=direccion_institucion,
                    telefono=telefono_institucion,
                    observaciones=observaciones_institucion
                )
                
                nuevo_jinete_amazona = board.JineteAmazona.create_JineteAmazona(JineteAmazona,
                    nombre=nombre,
                    apellido=apellidos,
                    dni=dni,
                    domicilio=nuevo_domicilio.id,
                    telefono=telefono,
                    localidad_nacimiento= localidad_nacimiento,
                    fecha_nacimiento=fecha_nacimiento,
                    contacto_emergencia_id=contacto.id,
                    tiene_deuda=tiene_deuda,
                    becado=becado,
                    porcentaje_beca=porcentaje_beca, 
                    profesionales_asociados=profesionales_asociados,
                    certificado_discapacidad=certificado_discapacidad,
                    diagnostico_discapacidad=diagnostico_final,
                    provincia_nacimiento=provincia_nacimiento,
                    tipo_discapacidad=tipo_discapacidad,
                    asignacion_familiar=asignacion_familiar,
                    tipo_asignacion = tipo_asignacion,
                    situaciones_previsional_id = nueva_situacionPrevisional.id,
                    institucion_escolar_id=nueva_institucion.id,
                    grado_actual=grado_actual,
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
                
                
                tipos_parentesco = request.form.getlist('parentesco[]')
                nombres_familiar = request.form.getlist('nombre_familiar[]')
                apellidos_familiar = request.form.getlist('apellido_familiar[]')
                DNIs_familiar = request.form.getlist('dni_familiar[]')
                celulares = request.form.getlist('celular_familiar[]')
                email_familiares = request.form.getlist('email_familiar[]')
                nivel_escolaridad = request.form.getlist('nivel_escolaridad[]')
                ocupaciones_familiar = request.form.getlist('ocupacion_familiar[]')
                calle_familiar = request.form.getlist('calle_familiar[]')
                numero_familiar = request.form.getlist('numero_familiar[]')
                depto_familiar = request.form.getlist('depto_familiar[]')
                localidad_familiar = request.form.getlist('localidad_familiar[]')
                provincia_familiar = request.form.getlist('provincia_familiar[]')

                for i in range(len(nombres_familiar)):
                    if check_String(tipos_parentesco[i],nombres_familiar[i],apellidos_familiar[i],DNIs_familiar[i],celulares[i],ocupaciones_familiar[i],calle_familiar[i],numero_familiar[i],localidad_familiar[i]) and check_nivel_escolaridad(nivel_escolaridad[i]):
                        
                        domicilio_familiar = board.domicilio.create_domicilio(
                            board.domicilio,
                            calle =  calle_familiar[i],
                            numero = numero_familiar[i],
                            depto = depto_familiar[i],
                            localidad = localidad_familiar[i],
                            provincia = provincia_familiar[i],
                            )
                        nuevo_familiar = FamiliarResponsable.create_familiar_responsable(
                        parentesco=tipos_parentesco[i],
                        nombre=nombres_familiar[i],
                        apellido=apellidos_familiar[i],
                        dni=DNIs_familiar[i],
                        celular=celulares[i],
                        email=email_familiares[i],
                        nivel_escolaridad=nivel_escolaridad[i],
                        actividad_ocupacion=ocupaciones_familiar[i],
                        domicilio=domicilio_familiar.id,
                        jinete_amazona_id = nuevo_jinete_amazona.id,
                    )
                    else:
                        return redirect(url_for("jinete_amazona.create"))

                if not tipos_documento == ['']:
                    for i in range(len(tipos_documento)):
                        tipo_doc = tipos_documento[i]
                        tipo_entrada = tipos_entrada[i]  
                        archivo = documento_controller.create(
                                file = archivos[i],
                                link = enlaces[i], 
                                document_type=tipo_doc, 
                                titular_id = nuevo_jinete_amazona.id,
                                tipo_titular = TipoTitular.jya, 
                                tipo_entrada = tipo_entrada
                        )
               
                flash("Jinete/Amazona creado exitosamente", "success")
                return redirect(url_for("jinete_amazona.index"))  
            except ValueError as e:
                flash(str(e), "error")
                return redirect(url_for("jinete_amazona.create"))   
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error en el campo {getattr(form, field).label.text}: {error}", "error")
            return redirect(url_for("jinete_amazona.create"))  
    tipos_docs=TipoDocumento.get_tipo_doc_jinetes()
    
    return render_template("jinete_amazona/create.html.jinja", tipos_docs=tipos_docs,form_data={}, diagnostico_discapacidad=diagnosticos, tipo_discapacidad=TipoDiscapacidad, tipo_asignacion = TipoAsignacion, tipo_pension = TipoPension, tipo_escolaridad = TipoEscolaridad, propuesta_trabajo = TipoPropuesta,  condicion = TipoCondicion, sede = TipoSede, tipo_provincia = TipoProvincia, empleado = empleado, caballos=caballos,form=form)

    


@bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
@check_permission("update_jinete")
def update(id):
    """
    Actualiza la información de un jinete o amazona específico.

    Esta función permite modificar los datos de un jinete o amazona basado en el 
    identificador proporcionado. Recupera los datos actuales, maneja la 
    actualización a través de un formulario y redirige a la página de índice 
    si la actualización es exitosa.

    Parámetros:
        - id (int): El identificador del jinete o amazona a actualizar.

    Retorna:
        - redirect: Redirige a la página de índice si la actualización es exitosa.
        - render_template: Renderiza la plantilla de actualización con datos actuales
                          y posibles errores si ocurre una excepción.
    """
    jinete_amazona = board.JineteAmazona.get_jinete_amazona(id)
    
    
    if not jinete_amazona:
        return redirect(url_for("jinete_amazona.index"))
    empleado = Empleado.get_empleado_activos()
    caballos = ejemplar.get_all_ejemplar()
    direccion_domicilio = board.domicilio.get_domicilio(jinete_amazona.domicilio)
    contacto_emergencia = board.contacto_emergencia.get_contacto_emergencia(jinete_amazona.contacto_emergencia_id)
    situacion_previsional = SituacionPrevisional.get_situacion_previsional(jinete_amazona.situacion_previsional_id)
    institucion_escolar = InstitucionEscolar.get_institucion_escolar(jinete_amazona.institucion_escolar_id)
    profesor = Empleado.get_empleado_id(jinete_amazona.profesor_id)
    auxiliar = Empleado.get_empleado_id(jinete_amazona.auxiliar_id)
    conductor = Empleado.get_empleado_id(jinete_amazona.conductor_id)
    caballo = ejemplar.get_ejemplar_by_id(jinete_amazona.caballo_id)
    form = JineteAmazonaForm(obj=jinete_amazona)


    if request.method == "POST":
        if form.validate_on_submit():
           
            try:
                nombre = form.nombre.data
                apellido = form.apellido.data
                dni = form.dni.data
                telefono = form.telefono.data
                fecha_nacimiento = form.fecha_nacimiento.data
                localidad_nacimiento = form.localidad_nacimiento.data
                provincia_nacimiento = form.provincia_nacimiento.data
                porcentaje_beca = form.porcentaje_beca.data
                profesionales_asociados = form.profesionales_asociados.data
                contacto_nombre = form.contacto_nombre.data
                contacto_telefono = form.contacto_telefono.data
                diagnostico_discapacidad = form.diagnostico_discapacidad.data
                tipo_discapacidad = form.tipo_discapacidad.data
                tipo_asignacion = form.tipo_asignacion.data
                tipo_pension = form.tipo_pension.data
                grado_actual = form.grado_actual.data
                propuesta_trabajo = form.propuesta_trabajo.data
                condicion = form.condicion.data
                sede = form.sede.data
                
                becado_value = form.becado.data
                becado = True if becado_value == 'True' else False
                
                tiene_deuda_value = form.tiene_deuda.data
                tiene_deuda = True if tiene_deuda_value == 'True' else False
                
                certificado_discapacidad_value = form.certificado_discapacidad.data
                certificado_discapacidad = True if certificado_discapacidad_value == 'True' else False
                
                asignacion_familiar_value = form.asignacion_familiar.data
                asignacion_familiar = True if asignacion_familiar_value == 'True' else False
                
                pensionado_value = form.pensionado.data
                pensionado = True if pensionado_value == 'True' else False

                # Situación Previsional
                obra_social = form.obra_social.data or situacion_previsional.obra_social
                numero_afiliado = form.numero_afiliado.data or situacion_previsional.numero_afiliado
                observaciones = form.observaciones.data or situacion_previsional.observaciones

                
                posee_curatela_value = form.posee_curatela.data
                posee_curatela = True if posee_curatela_value == 'True' else False

                # Institución Escolar
                nombre_institucion = form.nombre_institucion.data
                direccion_institucion = form.direccion_institucion.data
                telefono_institucion = form.telefono_institucion.data
                observaciones_institucion = form.observaciones_institucion.data

                # Contacto de emergencia
                contacto_nombre = form.contacto_nombre.data
                contacto_telefono = form.contacto_telefono.data

                # Domicilio del jinete
                calle = form.calle.data
                numero = form.numero.data
                depto = form.depto.data
                localidad = form.localidad.data
                provincia = form.provincia.data

                dias_trabajo = form.dias_trabajo.data
                profesor_id = request.form.get("profesor_id")
                auxiliar_id = request.form.get("auxiliar_id")
                conductor_id = request.form.get("conductor_id")
                caballo_id = request.form.get("caballo_id")
                board.JineteAmazona.update_jinete_amazona( 
                    id=id,
                    nombre=nombre,
                    apellido=apellido,
                    dni=dni,
                    localidad_nacimiento=localidad_nacimiento,
                    provincia_nacimiento=provincia_nacimiento,
                    domicilio=direccion_domicilio.id,
                    telefono=telefono,
                    fecha_nacimiento=fecha_nacimiento,
                    tiene_deuda=tiene_deuda,
                    becado=becado,
                    porcentaje_beca=porcentaje_beca,
                    profesionales_asociados=profesionales_asociados,
                    certificado_discapacidad = certificado_discapacidad,
                    diagnostico_discapacidad = diagnostico_discapacidad,
                    tipo_discapacidad = tipo_discapacidad,
                    asignacion_familiar = asignacion_familiar,
                    tipo_asignacion = tipo_asignacion,
                    pensionado = pensionado,
                    tipo_pension = tipo_pension,
                    grado_actual = grado_actual,
                    situacion_previsional_id=situacion_previsional.id,
                    institucion_escolar_id=institucion_escolar.id,
                    contacto_emergencia_id=contacto_emergencia.id,
                    propuesta_trabajo = propuesta_trabajo,
                    condicion = condicion,
                    sede = sede,
                    dias_trabajo = dias_trabajo,
                    profesor_id = profesor_id,
                    auxiliar_id = auxiliar_id,
                    conductor_id = conductor_id,
                    caballo_id = caballo_id,
                )
                
                
                
                
                situacion_previsional = SituacionPrevisional.update_situacion_previsional(
                    SituacionPrevisional,
                    id = situacion_previsional.id,
                    obra_social = obra_social,
                    numero_afiliado = numero_afiliado,
                    posee_curatela= posee_curatela,
                    observaciones=observaciones,
                )

                
                
                InstitucionEscolar.update_institucion_escolar(
                    id = institucion_escolar.id,
                    nombre = nombre_institucion,
                    direccion= direccion_institucion,
                    telefono = telefono_institucion,
                    observaciones= observaciones_institucion,
                )
                
                board.domicilio.update_domicilio(
                    direccion_domicilio.id,
                    calle=calle,
                    numero=numero,
                    depto=depto,
                    localidad=localidad,
                    provincia=provincia
                )

                board.contacto_emergencia.update_contacto_emergencia(
                    contacto_emergencia.id, 
                    nombre=contacto_nombre,
                    telefono=contacto_telefono
                )

                
                flash("Jinete/Amazona editado exitosamente", "success")
                return redirect(url_for("jinete_amazona.index"))
            except ValueError as e:
                flash(str(e), "error")
                return render_template("jinete_amazona/update.html.jinja",
                                   jinete_amazona=jinete_amazona,
                                   domicilio=direccion_domicilio,
                                   contacto_emergencia=contacto_emergencia,
                                   form_data=request.form)

    return render_template("jinete_amazona/update.html.jinja", jinete_amazona=jinete_amazona,profesor = profesor, auxiliar = auxiliar, conductor = conductor, caballo = caballo,situacion_previsional=situacion_previsional,diagnostico_discapacidad=diagnosticos, tipo_discapacidad=TipoDiscapacidad, tipo_asignacion = TipoAsignacion, tipo_pension = TipoPension, tipo_escolaridad = TipoEscolaridad, propuesta_trabajo = TipoPropuesta,  condicion = TipoCondicion, sede = TipoSede,caballos=caballos, empleado=empleado, provincia=TipoProvincia, form=form, institucion_escolar = institucion_escolar, direccion_domicilio=direccion_domicilio, contacto_emergencia=contacto_emergencia)
 
@bp.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
@check_permission("delete_jinete")
 
def delete(id):
    """
    Elimina un jinete o amazona y sus datos asociados.

    Esta función se ejecuta cuando se recibe una solicitud POST. Busca el jinete 
    por su identificador, elimina todos los documentos asociados, y borra 
    la situación previsional e institución escolar, si existen. 

    Parámetros:
        - id (int): El identificador del jinete o amazona a eliminar.

    Retorna:
        - redirect: Redirige a la página de índice de jinetes/amazonas tras 
                    eliminar correctamente el registro.
    """
    if request.method == 'POST':
        try:
            jinete = JineteAmazona.query.get(id)
            if not jinete:
                raise ValueError("Jinete no encontrado")
                
            FamiliarResponsable.delete_all_by_jinete(id)


            for documento in jinete.documentos:
                Documento.delete(documento) 

            JineteAmazona.delete_jinete(id)
            
            if jinete.situacion_previsional_id:
                SituacionPrevisional.delete_situacion_previsional(jinete.situacion_previsional_id)
            
            if jinete.institucion_escolar_id:
                InstitucionEscolar.delete_institucion_escolar(jinete.institucion_escolar_id)
            
            flash("Jinete/amazona eliminado correctamente", "success")
        except Exception as e:  
            flash(str(e), "error")
        finally:
            return redirect(url_for("jinete_amazona.index"))

@bp.route("/<int:id>", methods=["GET"])
@login_required
@check_permission("show_jinete")

def show(id):
    """
    Muestra la información detallada de un jinete o amazona.

    Recupera y presenta los detalles de un jinete o amazona, incluyendo 
    su dirección, contacto de emergencia, situación previsional, 
    información del profesor, auxiliar y conductor, así como 
    los familiares responsables y documentos asociados.

    Parámetros:
        - id (int): El identificador del jinete o amazona a mostrar.

    Retorna:
        - render_template: Renderiza la plantilla de visualización 
                           con todos los detalles del jinete o amazona.
    """
    jinete = JineteAmazona.get_jinete_amazona(id)
    
    if jinete:
        direccion = board.domicilio.get_domicilio(jinete.domicilio)
        contacto = board.contacto_emergencia.get_contacto_emergencia(jinete.contacto_emergencia_id) 
        situacion_previsional = SituacionPrevisional.get_situacion_previsional(jinete.situacion_previsional_id)
        profesor = Empleado.get_empleado_id(jinete.profesor_id)
        auxiliar = Empleado.get_empleado_id(jinete.auxiliar_id)
        conductor = Empleado.get_empleado_id(jinete.conductor_id)
        familiares = jinete.familiares_responsables  
        documentos = jinete.documentos
        tiene_deuda = jinete.tiene_deuda  
        becado = jinete.becado  
        porcentaje_beca = jinete.porcentaje_beca 

    return render_template(
        "jinete_amazona/show.html.jinja", 
        jinete_amazona=jinete, 
        direccion=direccion, 
        contacto=contacto,
        situacion_previsional=situacion_previsional,
        familiares=familiares,
        documentos=documentos,
        profesor=profesor,
        auxiliar=auxiliar,
        conductor =conductor,
        tiene_deuda=tiene_deuda,
        becado=becado,
        porcentaje_beca=porcentaje_beca
    )



diagnosticos = [
    "ECNE",
    "Lesión post-traumática",
    "Mielomeningocele",
    "Esclerosis Múltiple",
    "Escoliosis Leve",
    "Secuelas de ACV",
    "Discapacidad Intelectual",
    "Trastorno del Espectro Autista",
    "Trastorno del Aprendizaje",
    "Trastorno por Déficit de Atención/Hiperactividad",
    "Trastorno de la Comunicación",
    "Trastorno de Ansiedad",
    "Síndrome de Down",
    "Retraso Madurativo",
    "Psicosis",
    "Trastorno de Conducta",
    "Trastornos del ánimo y afectivos",
    "Trastorno Alimentario",
    "OTRO",
    ]


def check_String(tipos_parentesco,nombres_familiar,apellidos_familiar,DNIs_familiar,celulares,ocupaciones_familiar,calle_familiar,numero_familiar,localidad_familiar):
    if not tipos_parentesco or not nombres_familiar or not apellidos_familiar or not DNIs_familiar or not celulares or not ocupaciones_familiar or not calle_familiar or not numero_familiar or not localidad_familiar:
        flash("Debe completar todos los campos de los familiares responsables", "error")
        return False
    else: 

        if len(tipos_parentesco) > 50:
            flash("El parentesco del familiar responsable no puede superar los 50 caracteres", "error")
            return False
        if len(nombres_familiar) > 50:
            flash("El nombre del familiar responsable no puede superar los 50 caracteres", "error")
            return False
        if len(apellidos_familiar) > 50:
            flash("El apellido del familiar responsable no puede superar los 50 caracteres", "error")
            return False
        if len(DNIs_familiar) != 8:
            flash("El DNI del familiar responsable debe tener 8 caracteres", "error")
            return False
        if len(celulares) > 50 or len(celulares) <= 7:
            flash("El celular del familiar responsable debe tener entre 7 y 50 caracteres", "error")
            return False
        if len(ocupaciones_familiar) > 100:
            flash("La ocupación del familiar responsable no puede superar los 100 caracteres", "error")
            return False
        if len(calle_familiar) > 50:
            flash("La calle del familiar responsable no puede superar los 50 caracteres", "error")
            return False
        if len(numero_familiar) > 10:
            flash("El número del familiar responsable no puede superar los 10 caracteres", "error")
            return False
        if len(localidad_familiar) > 50:
            flash("La localidad del familiar responsable no puede superar los 50 caracteres", "error")
            return False
        

    return True


def check_nivel_escolaridad(nivel_escolaridad):
    if not nivel_escolaridad:
        flash("Debe seleccionar un nivel de escolaridad", "error")
        return False
    return True