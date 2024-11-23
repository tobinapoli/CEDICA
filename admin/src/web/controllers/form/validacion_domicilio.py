
from wtforms.validators import ValidationError

def validate_direccion(form, field):
    if len(field.data) > 50:
        raise ValidationError("La longitud máxima para la calle es de 50 caracteres.")

def validate_numero(form, field):
    if len(field.data) > 10:
        raise ValidationError("La longitud máxima para el número es de 10 caracteres.")

def validate_localidad(form, field):
    if len(field.data) > 50:
        raise ValidationError("La longitud máxima para la localidad es de 50 caracteres.")

def validate_depto(form, field):
    if len(field.data) > 10:
        raise ValidationError("La longitud máxima para el departamento es de 10 caracteres.")