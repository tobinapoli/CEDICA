from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, EmailField
from wtforms.validators import Length, DataRequired, Optional, Email
from src.core.board.familiares_responsables import TipoEscolaridad
from src.core.board.domicilio import TipoProvincia
from src.web.controllers.form.validacion_contacto import validate_telefono_contacto
from src.web.controllers.form.validacion_domicilio import validate_direccion, validate_numero, validate_localidad, validate_depto

class FamiliarForm(FlaskForm):
    parentesco = StringField("Parentesco", validators=[DataRequired(message="Este campo es obligatorio"), Length(min=1, max=50, message="Debe tener entre 1 y 50 caracteres")])
    nombre = StringField("Nombre", validators=[DataRequired(message="Este campo es obligatorio"), Length(min=1, max=50, message="Debe tener entre 1 y 50 caracteres")], render_kw={"pattern": "[a-zA-Z]+"}, description="Solo letras")
    apellido = StringField("Apellido", validators=[DataRequired(message="Este campo es obligatorio"), Length(min=1, max=50, message="Debe tener entre 1 y 50 caracteres")], render_kw={"pattern": "[a-zA-Z]+"}, description="Solo letras")
    dni = StringField("DNI", validators=[DataRequired(message="Este campo es obligatorio"), Length(min=8, max=8, message="Debe tener 8 caracteres")], render_kw={"pattern": "[0-9]{8}"})
    celular = StringField("Celular actual", validators=[DataRequired(message="Este campo es obligatorio"), Length(max=50, message="Debe tener como máximo 50 caracteres"), validate_telefono_contacto])
    actividad_ocupacion = StringField("Ocupación", validators=[DataRequired(message="Este campo es obligatorio"), Length(min=1, max=50, message="Debe tener entre 1 y 50 caracteres")])
    email = EmailField("Email", validators=[DataRequired(message="Este campo es obligatorio"), Length(min=1, max=50, message="Debe tener entre 1 y 50 caracteres"), Email(message="Debe ser un email válido")])
    
    
    calle = StringField("Calle", validators=[DataRequired(message="Este campo es obligatorio"), validate_direccion])
    numero = StringField("Número", validators=[DataRequired(message="Este campo es obligatorio"), validate_numero])
    depto = StringField("Departamento", validators=[Optional(), validate_depto])
    localidad = StringField("Localidad", validators=[DataRequired(message="Este campo es obligatorio"), validate_localidad])
    provincia = SelectField("provincia", choices=[(choice.name, choice.value) for choice in TipoProvincia], validators=[DataRequired(message="Este campo es obligatorio")])
    nivel_escolaridad = SelectField("Nivel de Escolaridad", choices=[(choice.name, choice.value) for choice in TipoEscolaridad], validators=[DataRequired(message="Este campo es obligatorio")])