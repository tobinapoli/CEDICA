from typing import Optional
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import Optional,DataRequired, Email, Length, Regexp, ValidationError
from src.core.board.rol import Rol
from src.core.auth import User  

class UserUpdateForm(FlaskForm):
    
    new_email = StringField("Correo electrónico", validators=[
        Optional(),
        Email(message="Formato de correo no válido.")
    ])
    alias = StringField("Alias", validators=[
        Optional(),
        Length(max=50, message="El alias no debe exceder los 50 caracteres.")
        
    ])
    password = PasswordField("Contraseña", validators=[
        Optional(),
        Length(min=8, message="La contraseña debe tener al menos 8 caracteres."),
        Length(max=255, message="La contraseña no debe exceder los 255 caracteres."),
        Regexp(
            r'^(?=.*\d).{8,}$',
            message="La contraseña debe contener al menos un número."
        )
    ])
    
    activo = SelectField('activo:',choices=[('True', 'Sí'), ('False', 'No')],default='True',  validators=[DataRequired()])
    registroAprobado = SelectField('registroAprobado:',choices=[('True', 'Sí'), ('False', 'No')],default='True',  validators=[DataRequired()])
    
    rol_id = SelectField('Rol', choices=[], validators=[Optional()])
    submit = SubmitField("Actualizar Usuario")
    
    
    def validate_rol_id(self, field):
        if field.data == 0:
            raise ValidationError("Debe seleccionar un rol válido.")
