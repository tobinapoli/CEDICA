from wtforms.validators import Optional
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField, DateField, FieldList, FormField, SelectMultipleField
from wtforms.validators import DataRequired, Length, NumberRange
from datetime import datetime
from wtforms.validators import ValidationError
from src.core.board.jinete_amazona import TipoAsignacion, TipoCondicion, TipoDiscapacidad, TipoPension, TipoPropuesta, TipoSede
from src.core.board.domicilio import TipoProvincia
from src.web.controllers.form.validacion_domicilio import validate_direccion, validate_numero, validate_localidad, validate_depto
from src.web.controllers.form.validacion_contacto import validate_nombre_contacto, validate_telefono_contacto
from src.web.controllers.form.familiares_form import FamiliarForm


    
class JineteAmazonaForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(message="El nombre es obligatorio."), Length(min=1, max=50, message="El nombre debe tener entre 1 y 50 caracteres.")])
    apellido = StringField("Apellido", validators=[DataRequired(message="El apellido es obligatorio."), Length(min=1, max=50, message="El apellido debe tener entre 1 y 50 caracteres.")])
    dni = StringField("DNI", validators=[DataRequired(message="El DNI es obligatorio."), Length(min=8, max=8, message="El DNI debe tener exactamente 8 caracteres.")], render_kw={"pattern": "[0-9]{8}"})
    telefono = StringField("Telefono", validators=[DataRequired(message="El teléfono es obligatorio."), Length(min=7, max=50, message="El teléfono debe tener entre 7 y 50 caracteres.")])
    localidad_nacimiento = StringField("Localidad de Nacimiento", validators=[DataRequired(message="La localidad de nacimiento es obligatoria."), Length(min=1, max=50, message="La localidad de nacimiento debe tener entre 1 y 50 caracteres.")])
    becado = SelectField('Becado:',choices=[('True', 'Sí'), ('False', 'No')],default='False',  validators=[DataRequired()])
    porcentaje_beca = IntegerField("Porcentaje de Beca", validators=[Optional(), NumberRange(min=0, max=100, message="El porcentaje de beca debe estar entre 0 y 100.")])
    profesionales_asociados = StringField("Profesionales Asociados", validators=[DataRequired(message="Los profesionales asociados son obligatorios."), Length(min=1, max=50, message="Los profesionales asociados deben tener entre 1 y 50 caracteres.")])
    certificado_discapacidad = SelectField("Certificado de Discapacidad", choices=[('True', 'Sí'), ('False', 'No')],default='True', validators=[DataRequired(message="El campo de certificado de discapacidad es obligatorio.")])
    tipo_discapacidad = SelectField("Tipo de Discapacidad", choices=[(choice.name, choice.value) for choice in TipoDiscapacidad], validators=[Optional()])
    diagnostico_discapacidad = StringField("Diagnóstico de Discapacidad", validators=[Optional(), Length(max=50, message="El diagnóstico de discapacidad como maximo 50 caracteres.")])
    diagnostico_otro = StringField("Diagnóstico Otro", validators=[Optional(), Length(min=1, max=50, message="El diagnóstico debe tener entre 1 y 50 caracteres.")])
    asignacion_familiar = SelectField("Asignación Familiar", choices=[('True', 'Sí'), ('False', 'No')],default='True', validators=[DataRequired(message="El campo de asignación familiar es obligatorio.")])
    tipo_asignacion = SelectField("Tipo de Asignación", choices=[(choice.name, choice.value) for choice in TipoAsignacion], validators=[Optional()])
    pensionado = SelectField("Pensionado", choices=[('True', 'Sí'), ('False', 'No')],default='True', validators=[DataRequired(message="El campo de pensionado es obligatorio.")])
    tipo_pension = SelectField("Tipo de Pensión", choices=[(choice.name, choice.value) for choice in TipoPension], validators=[Optional()])
    grado_actual = StringField("Grado Actual", validators=[DataRequired(message="El grado actual es obligatorio."), Length(min=1, max=50, message="El grado actual debe tener entre 1 y 50 caracteres.")])
    tiene_deuda = SelectField("Tiene Deuda", choices=[('True', 'Sí'), ('False', 'No')],default='False', validators=[DataRequired(message="El campo de tiene deuda es obligatorio.")])
    provincia_nacimiento = SelectField("Provincia de Nacimiento", choices=[(choice.name, choice.value) for choice in TipoProvincia], validators=[DataRequired()])
    provincia = SelectField("provincia", choices=[(choice.name, choice.value) for choice in TipoProvincia], validators=[DataRequired()])
   
    # Situación Previsional
    obra_social = StringField("Obra Social", validators=[DataRequired(message="La obra social es obligatoria."), Length(min=4, max=50, message="La obra social debe tener entre 4 y 50 caracteres.")])
    numero_afiliado = StringField("Número de Afiliado", validators=[DataRequired(message="El número de afiliado es obligatorio."), Length(min=8, max=50, message="El número de afiliado debe tener entre 8 y 50 caracteres.")])
    posee_curatela = SelectField("Posee Curatela", choices=[('True', 'Sí'), ('False', 'No')],default='False', validators=[DataRequired(message="El campo de posee curatela es obligatorio.")])
    observaciones = StringField("Observaciones", validators=[Optional(), Length(max=255, message="Las observaciones no deben exceder los 255 caracteres.")])
    
    # Domicilio
    calle = StringField("calle", validators=[DataRequired(message="La calle es obligatoria."), validate_direccion])
    numero = StringField("numero", validators=[DataRequired(message="El número es obligatorio."), validate_numero])
    localidad = StringField("localidad", validators=[DataRequired(message="La localidad es obligatoria."), validate_localidad])
    depto = StringField("depto", validators=[Optional(), validate_depto])
    
    # Contacto de Emergencia
    contacto_nombre = StringField("Nombre de Contacto", validators=[DataRequired(message="El nombre del contacto es obligatorio."), validate_nombre_contacto])
    contacto_telefono = StringField("Teléfono de Contacto", validators=[DataRequired(message="El teléfono del contacto es obligatorio."),validate_telefono_contacto])
    
    #Institucion Escolar
    nombre_institucion = StringField("Nombre de la institucion", validators=[DataRequired(message="El nombre es obligatorio."), Length(min=1, max=100, message="El nombre debe tener entre 1 y 100 caracteres.")])
    direccion_institucion = StringField("Direccion de la institucion", validators=[DataRequired(message="La dirección es obligatoria."), Length(min=1, max=150, message="La dirección debe tener entre 1 y 150 caracteres.")])
    telefono_institucion = StringField("Telefono de la institucion", validators=[Optional(), Length(min=7, max=50, message="El teléfono debe tener entre 7 y 50 caracteres.")])
    observaciones_institucion = StringField("Observaciones de la institucion", validators=[Optional(), Length(max=255, message="Las observaciones no deben exceder los 255 caracteres.")])
    
    

    # Trabajo en la institucion
    propuesta_trabajo = SelectField("Propuesta de trabajo", choices=[(choice.name, choice.value) for choice in TipoPropuesta], validators=[DataRequired()])
    
    condicion = SelectField("Condicion", choices=[(choice.name, choice.value) for choice in TipoCondicion], validators=[DataRequired()])
    sede = SelectField("Sede", choices=[(choice.name, choice.value) for choice in TipoSede], validators=[DataRequired()])
    dias_trabajo = SelectMultipleField("Días de Trabajo", choices=[
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miercoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sabado', 'Sábado'),
        ('Domingo', 'Domingo')
    ], validators=[DataRequired(message="Debe seleccionar al menos un día de trabajo.")])
    
    def validate_dias_trabajo(form, field):
        if not field.data:
            raise ValidationError("Debe seleccionar al menos un día de trabajo.")
    
    
    def validate_fecha_nacimiento(form, field):
        if field.data is None:
            raise ValidationError("La fecha de nacimiento es obligatoria.")
        if field.data >= datetime.today().date():
            raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        if field.data <= (datetime.today().date().replace(year=datetime.today().year - 100)):
            raise ValidationError("La fecha de nacimiento no puede ser hace más de 100 años.")
        
    fecha_nacimiento = DateField("Fecha de Nacimiento", validators=[DataRequired(message="La fecha de nacimiento es obligatoria."), validate_fecha_nacimiento])
