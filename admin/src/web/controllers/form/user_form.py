from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError
from src.core.board.rol import Rol
from src.core.auth import User  

class UserCreateForm(FlaskForm):
    email = StringField("Correo electrónico", validators=[
        DataRequired(message="El correo es obligatorio."),
        Length(max=50, message="El correo no debe exceder los 50 caracteres."),
        Email(message="Formato de correo no válido.")
    ])
    alias = StringField("Alias", validators=[
        DataRequired(message="El alias es obligatorio."),
        Length(max=50, message="El alias no debe exceder los 50 caracteres.")
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=8, message="La contraseña debe tener al menos 8 caracteres."),
        Length(max=255, message="La contraseña no debe exceder los 255 caracteres."),
        Regexp(
            r'^(?=.*\d).{8,}$',
            message="La contraseña debe contener al menos un número."
        )
    ])
    rol_id = SelectField("Rol", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Crear Usuario")
    
    
    def validate_rol_id(self, field):
        if field.data == 0:
            raise ValidationError("Debe seleccionar un rol válido.")
   
    def validate_email(self, email):
        user = User.get_by_email(str(email))
        if user:
            raise ValidationError("El correo ya está registrado.")

