#make 2 def para validar el formulario de contacto

from wtforms.validators import ValidationError

def validate_nombre_contacto(form, field):
    if len(field.data) > 50:
        raise ValidationError("La longitud máxima para el nombre del contacto es de 50 caracteres.")

def validate_telefono_contacto(form, field):
    if len(field.data) > 50 and len(field.data) < 7:
        raise ValidationError("La longitud máxima para el teléfono del contacto es de 50 caracteres.")