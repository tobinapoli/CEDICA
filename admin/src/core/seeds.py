from src.core.board.domicilio import TipoProvincia
from src.core.board.situacion_previsional import SituacionPrevisional
from src.core.board.contenido import Estado as ContenidoEstado
from src.core import board
from src.core import auth


def run():
    # Crear los usuarios con sus respectivos roles y permisos
    system_admin = board.Rol.create_role(nombre="System Admin")
    admin_rol = board.Rol.create_role(nombre="Gestion Administrativa") 
    voluntariado_rol = board.Rol.create_role(nombre="Voluntariado")
    tecnica_rol = board.Rol.create_role(nombre="Tecnica") 
    ecuestre_rol = board.Rol.create_role(nombre="Ecuestre") 
    editor_rol = board.Rol.create_role(nombre="Editor")

    # Crear los permisos
    # Permisos de usuario
    permiso_crear_usuario = board.create_permission(nombre="create_user")
    permiso_editar_usuario = board.create_permission(nombre="edit_user")
    permiso_eliminar_usuario = board.create_permission(nombre="delete_user")
    permiso_index_usuario = board.create_permission(nombre="index_user")
    permiso_ver_usuario = board.create_permission(nombre="view_user")
    permiso_aceptar_usuario = board.create_permission(nombre="accept_user")
    
    # Permisos de empleados
    permiso_crear_empleado = board.create_permission(nombre="create_empleado")
    permiso_editar_empleado = board.create_permission(nombre="edit_empleado")
    permiso_eliminar_empleado = board.create_permission(nombre="delete_empleado")
    permiso_index_empleado = board.create_permission(nombre="index_empleado")
    permiso_ver_empleado = board.create_permission(nombre="view_empleado")
    
    # Permisos de cobros
    permiso_crear_cobro = board.create_permission(nombre="create_cobro")
    permiso_editar_cobro = board.create_permission(nombre="edit_cobro")
    permiso_eliminar_cobro = board.create_permission(nombre="delete_cobro")
    permiso_ver_cobro = board.create_permission(nombre="view_cobro")
    permiso_index_cobro = board.create_permission(nombre="index_cobro")

    #permiso de contactos
    permiso_crear_consulta = board.create_permission(nombre="create_consulta")
    permiso_editar_consulta = board.create_permission(nombre="edit_consulta")
    permiso_eliminar_consulta = board.create_permission(nombre="delete_consulta")
    permiso_ver_consulta = board.create_permission(nombre="show_consulta")
    permiso_index_consulta = board.create_permission(nombre="index_consulta")

    #permiso de pagos
    permiso_crear_pago = board.create_permission(nombre="create_pago")
    permiso_editar_pago = board.create_permission(nombre="edit_pago")
    permiso_eliminar_pago = board.create_permission(nombre="delete_pago")
    permiso_ver_pago = board.create_permission(nombre="show_pago")
    permiso_index_pago = board.create_permission(nombre="index_pago")
    
    # Permisos de ecuestre
    permiso_crear_ejemplar = board.create_permission(nombre="create_ejemplares")
    permiso_editar_ejemplar = board.create_permission(nombre="edit_ejemplares")
    permiso_eliminar_ejemplar = board.create_permission(nombre="delete_ejemplares")
    permiso_index_ejemplar = board.create_permission(nombre="index_ejemplares")
    permiso_ver_ejemplar = board.create_permission(nombre="view_ejemplares")
    
    # Permisos de jinetes/amazonas
    permiso_crear_jinete = board.create_permission(nombre="create_jinete")
    permiso_editar_jinete = board.create_permission(nombre="update_jinete")
    permiso_eliminar_jinete = board.create_permission(nombre="delete_jinete")
    permiso_index_jinete = board.create_permission(nombre="index_jinete")
    permiso_ver_jinete = board.create_permission(nombre="show_jinete")
    
    # Permisos de familiares
    permiso_crear_familiar = board.create_permission(nombre="create_familiares")
    permiso_editar_familiar = board.create_permission(nombre="update_familiares")
    permiso_eliminar_familiar = board.create_permission(nombre="delete_familiares")
    permiso_index_familiar = board.create_permission(nombre="index_familiares")
    permiso_ver_familiar = board.create_permission(nombre="show_familiares")
    
    # Permisos de usuarios
    permiso_crear_usuario = board.create_permission(nombre="create_user")
    permiso_editar_usuario = board.create_permission(nombre="edit_user")
    permiso_eliminar_usuario = board.create_permission(nombre="delete_user")
    permiso_index_usuario = board.create_permission(nombre="index_user")
    permiso_ver_usuario = board.create_permission(nombre="view_user")
    
    # Permisos de contenido
    permiso_crear_contenido = board.create_permission(nombre="create_contenido")
    permiso_editar_contenido = board.create_permission(nombre="edit_contenido")
    permiso_eliminar_contenido = board.create_permission(nombre="delete_contenido")
    permiso_index_contenido = board.create_permission(nombre="index_contenido")
    permiso_ver_contenido = board.create_permission(nombre="view_contenido")
    
    permiso_ver_graficos = board.create_permission(nombre="view_graficos")
    permiso_ver_reportes = board.create_permission(nombre="view_reportes")
    permiso_index_reportes = board.create_permission(nombre="index_reportes")
    permiso_index_graficos = board.create_permission(nombre="index_graficos")

    

    # Permisos para administradores
    # Empleados
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_crear_empleado.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_editar_empleado.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_eliminar_empleado.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_ver_empleado.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_index_empleado.id)
    # Cobros
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_crear_cobro.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_editar_cobro.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_eliminar_cobro.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_ver_cobro.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_index_cobro.id)
    #contactos
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_crear_consulta.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_editar_consulta.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_eliminar_consulta.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_ver_consulta.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_index_consulta.id)
    # Pagos
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_crear_pago.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_editar_pago.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_eliminar_pago.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_ver_pago.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_index_pago.id)
    # Ecuestre
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_index_ejemplar.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_ver_ejemplar.id)
    # JyA
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_crear_jinete.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_editar_jinete.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_eliminar_jinete.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_index_jinete.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_ver_jinete.id)
    # Contenido
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_crear_contenido.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_editar_contenido.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_eliminar_contenido.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_index_contenido.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_ver_contenido.id)
    #graficos
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_ver_graficos.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_index_graficos.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_ver_reportes.id)
    board.assign_permission_to_role(rol_id=admin_rol.id, permiso_id=permiso_index_reportes.id)
    
    # Permisos rol editor
    # Contenido
    board.assign_permission_to_role(rol_id=editor_rol.id, permiso_id=permiso_crear_contenido.id)
    board.assign_permission_to_role(rol_id=editor_rol.id, permiso_id=permiso_editar_contenido.id)
    board.assign_permission_to_role(rol_id=editor_rol.id, permiso_id=permiso_eliminar_contenido.id)
    board.assign_permission_to_role(rol_id=editor_rol.id, permiso_id=permiso_index_contenido.id)
    board.assign_permission_to_role(rol_id=editor_rol.id, permiso_id=permiso_ver_contenido.id)
    

    
    # Permisos rol tecnica
    # Cobro
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_index_cobro.id)
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_ver_cobro.id)
    # Ecuestre
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_index_ejemplar.id)
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_ver_ejemplar.id)
    # JyA
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_index_jinete.id)
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_ver_jinete.id)
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_crear_jinete.id)
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_editar_jinete.id)
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_eliminar_jinete.id)
    #graficos
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_ver_graficos.id)
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_index_graficos.id)
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_ver_reportes.id)
    board.assign_permission_to_role(rol_id=tecnica_rol.id, permiso_id=permiso_index_reportes.id)
    
    # Permisos rol ecuestre
    # Ecuestre
    board.assign_permission_to_role(rol_id=ecuestre_rol.id, permiso_id=permiso_index_ejemplar.id)
    board.assign_permission_to_role(rol_id=ecuestre_rol.id, permiso_id=permiso_ver_ejemplar.id)
    board.assign_permission_to_role(rol_id=ecuestre_rol.id, permiso_id=permiso_crear_ejemplar.id)
    board.assign_permission_to_role(rol_id=ecuestre_rol.id, permiso_id=permiso_editar_ejemplar.id)
    board.assign_permission_to_role(rol_id=ecuestre_rol.id, permiso_id=permiso_eliminar_ejemplar.id)
    # Jya
    board.assign_permission_to_role(rol_id=ecuestre_rol.id, permiso_id=permiso_index_jinete.id)
    board.assign_permission_to_role(rol_id=ecuestre_rol.id, permiso_id=permiso_ver_jinete.id)
    
    #Permisos rol system admin
    #Usuarios
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_crear_usuario.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_editar_usuario.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_eliminar_usuario.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_index_usuario.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_ver_usuario.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_aceptar_usuario.id)
    # Empleados
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_crear_empleado.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_editar_empleado.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_eliminar_empleado.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_ver_empleado.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_index_empleado.id)
    # Cobros
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_crear_cobro.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_editar_cobro.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_eliminar_cobro.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_ver_cobro.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_index_cobro.id)
    #Contactos
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_crear_consulta.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_editar_consulta.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_eliminar_consulta.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_ver_consulta.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_index_consulta.id)
    # Pagos
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_crear_pago.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_editar_pago.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_eliminar_pago.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_ver_pago.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_index_pago.id)
    # Ecuestre
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_index_ejemplar.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_ver_ejemplar.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_crear_ejemplar.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_editar_ejemplar.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_eliminar_ejemplar.id)
    
    # JyA
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_crear_jinete.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_editar_jinete.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_eliminar_jinete.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_index_jinete.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_ver_jinete.id)
    # Contenido
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_crear_contenido.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_editar_contenido.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_eliminar_contenido.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_index_contenido.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_ver_contenido.id)

    #graficos
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_ver_graficos.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_index_graficos.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_ver_reportes.id)
    board.assign_permission_to_role(rol_id=system_admin.id, permiso_id=permiso_index_reportes.id)

    # Crear usuarios y asignar roles
    user1 = auth.User.create_user(alias='Juan', email='juan@gmail.com', password='adminpass', rol_id=admin_rol.id)
    user2 = auth.User.create_user(alias='Roberto', email='roberto@gmail.com', password='systemadminpass', rol_id=system_admin.id)
    user3 = auth.User.create_user(alias='Pedro', email='pedro@gmail.com', password='voluntariopass', rol_id=voluntariado_rol.id)
    user4 = auth.User.create_user(alias='Jose', email = 'jose@gmail.com', password = 'tecnicapass', rol_id=tecnica_rol.id)
    user5 = auth.User.create_user(alias='Lucas', email = 'lucas@gmail.com', password = 'ecuestrepass', rol_id=ecuestre_rol.id)
    user6 = auth.User.create_user(alias='Maria', email = 'maria@gmail.com', password = 'editorpass', rol_id=editor_rol.id)

    # Crear domicilios
    domicilio1 = board.create_domicilio(calle='Calle Falsa', numero='123', localidad='Ciudad A', provincia=TipoProvincia.CORDOBA)
    domicilio2 = board.create_domicilio(calle='Avenida Siempre Viva', numero='742', localidad='Ciudad B', provincia=TipoProvincia.CORDOBA)
    domicilio3 = board.create_domicilio(calle='Calle Luna', numero='456', localidad='Ciudad C', provincia=TipoProvincia.CORDOBA)

    # Crear puestos
    puesto1 = board.Puesto.create_puesto(nombre='Administrativo/a')
    puesto2 = board.Puesto.create_puesto(nombre='Terapeuta')
    puesto3 = board.Puesto.create_puesto(nombre='Conductor')
    puesto4 = board.Puesto.create_puesto(nombre='Auxiliar de pista')
    puesto5 = board.Puesto.create_puesto(nombre='Herrero')
    puesto6 = board.Puesto.create_puesto(nombre='Veterinario')
    puesto7 = board.Puesto.create_puesto(nombre='Entrenador de Caballos')
    puesto8 = board.Puesto.create_puesto(nombre='Domador')
    puesto9 = board.Puesto.create_puesto(nombre='Profesor de Equitación')
    puesto10 = board.Puesto.create_puesto(nombre='Docente de Capacitación')
    puesto11 = board.Puesto.create_puesto(nombre='Auxiliar de mantenimiento')
    puesto12 = board.Puesto.create_puesto(nombre='Otro')
    

    # Crear contactos de emergencia
    contacto1 = board.create_contacto_emergencia(nombre='Laura', telefono='123456789')
    contacto2 = board.create_contacto_emergencia(nombre='Miguel', telefono='987654321')
    contacto3 = board.create_contacto_emergencia(nombre='Sofia', telefono='456789123')

    # Crear empleados
    empleado1 = board.Empleado.create_empleado(
        nombre='Carlos', apellidos='Gomez', user_id=user1.id, dni='12345678', email='carlos@gmail.com',
        telefono='123456789', puesto_id=puesto1.id, fecha_ingreso='2023-01-01', obra_social='OSDE',
        numero_afiliado='123456', condicion='Efectivo', activo=True, domicilio=domicilio1.id,
        contacto_emergencia_id=contacto1.id, profesion="Terapista", fecha_egreso=None
    )

    empleado2 = board.Empleado.create_empleado(
        nombre='Ana', apellidos='Lopez', user_id=user2.id, dni='87654321', email='ana@gmail.com',
        telefono='987654321', puesto_id=puesto2.id, fecha_ingreso='2023-02-01', obra_social='Swiss Medical',
        numero_afiliado='654321', condicion='Efectivo', activo=True, domicilio=domicilio2.id,
        contacto_emergencia_id=contacto2.id, profesion="Docente", fecha_egreso=None
    )

    empleado3 = board.Empleado.create_empleado(
        nombre='Luis', apellidos='Martinez', user_id=user3.id, dni='11223344', email='luis@gmail.com',
        telefono='456789123', puesto_id=puesto3.id, fecha_ingreso='2023-03-01', obra_social='Galeno',
        numero_afiliado='789123', condicion='Efectivo', activo=True, domicilio=domicilio3.id,
        contacto_emergencia_id=contacto3.id, profesion="Terapista", fecha_egreso=None
    )

    situacion1 = SituacionPrevisional.create_situacion_previsional(
        obra_social="Obra Social de los Jubilados",
        numero_afiliado="123456789",
        posee_curatela=True,
        observaciones="El afiliado tiene una curatela activa y requiere atención especial."
    )

    medio_de_pago1 = board.create_medio_de_pago(nombre='Efectivo')
    medio_de_pago2 = board.create_medio_de_pago(nombre='Tarjeta de Crédito')
    medio_de_pago3 = board.create_medio_de_pago(nombre='Tarjeta de Débito')
    medio_de_pago4 = board.create_medio_de_pago(nombre='Transferencia Bancaria')


    # Crear pagos
    pago1 = board.create_pago(monto=1000, fecha='2023-01-01', beneficiario=None, tipo_de_pago='Proveedor', descripcion='Pago de sueldo')
    pago2 = board.create_pago(monto=1500, fecha='2023-02-01', beneficiario=None, tipo_de_pago='Proveedor', descripcion='Pago de sueldo')
    pago3 = board.create_pago(monto=2000, fecha='2023-03-01', beneficiario=None, tipo_de_pago='Proveedor', descripcion='Pago de luz')

    tipo_de_jinete1 = board.create_tipo_de_jinete(nombre='Hipoterapia')
    tipo_de_jinete2 = board.create_tipo_de_jinete(nombre='Equitacion')
    tipo_de_jinete3 = board.create_tipo_de_jinete(nombre='Deporte Ecuestre Adaptado')
    tipo_de_jinete4 = board.create_tipo_de_jinete(nombre='Monta Terapeutica')
    tipo_de_jinete4 = board.create_tipo_de_jinete(nombre='Actividades Recreativas')
    

    compra = board.tipo_adquisicion.compra
    donacion = board.tipo_adquisicion.donacion

    #crear ejemplares
    ejemplar1 = board.create_ejemplar(nombre='Caballo 1', fecha_nacimiento='2010-01-01', genero='Macho', raza='Cuarto de Milla', pela='Alazan', tipo_de_adquisicion=compra, fecha_ingreso='2023-01-01', sede='Sede 1', tipo_jinete = 1)
    ejemplar2 = board.create_ejemplar(nombre='Caballo 2', fecha_nacimiento='2015-01-01', genero='Hembra', raza='Pura Sangre', pela='Tordillo', tipo_de_adquisicion=donacion, fecha_ingreso='2023-02-01', sede='Sede 2', tipo_jinete = 2)
    ejemplar3 = board.create_ejemplar(nombre='Caballo 3', fecha_nacimiento='2020-01-01', genero='Macho', raza='Criollo', pela='Zaino', tipo_de_adquisicion=compra, fecha_ingreso='2023-03-01', sede='Sede 3', tipo_jinete = 3)
    ejemplar4 = board.create_ejemplar(nombre='Caballo 4', fecha_nacimiento='2010-01-01', genero='Macho', raza='Cuarto de Milla', pela='Alazan', tipo_de_adquisicion=compra, fecha_ingreso='2023-01-01', sede='Sede 1', tipo_jinete = 1)

    board.assign_empleado_to_ejemplar(empleado_id=empleado1.id, ejemplar_id=ejemplar1.id)
    board.assign_empleado_to_ejemplar(empleado_id=empleado2.id, ejemplar_id=ejemplar2.id)
    board.assign_empleado_to_ejemplar(empleado_id=empleado3.id, ejemplar_id=ejemplar3.id)
    
    contenido1 = board.Contenido.create_contenido(titulo='Titulo 1', copete='Copete 1', contenido='Contenido 1', user_email=user1.email, fecha_publicacion='2023-01-01', estado=ContenidoEstado.publicado)
    contenido2 = board.Contenido.create_contenido(titulo='Titulo 2', copete='Copete 2', contenido='Contenido 2', user_email=user2.email, fecha_publicacion='2023-02-01', estado=ContenidoEstado.borrador)
    contenido3 = board.Contenido.create_contenido(titulo='Titulo 3', copete='Copete 3', contenido='Contenido 3', user_email=user3.email, fecha_publicacion='2023-03-01', estado=ContenidoEstado.archivado)


