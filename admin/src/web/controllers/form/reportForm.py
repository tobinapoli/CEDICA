from wtforms.validators import Optional
from flask_wtf import FlaskForm
from wtforms import StringField,DateField
from wtforms.validators import DataRequired, Length, NumberRange
from datetime import datetime
from wtforms.validators import ValidationError



class reportForm(FlaskForm):
    
    jinete_nombre = StringField("Nombre del Jinete", validators=[Optional(), Length(max=50, message="El nombre del jinete no puede tener más de 50 caracteres.")])
    jinete_dni = StringField("DNI del Jinete", validators=[Optional(), Length(max=8, message="El DNI del jinete no puede tener más de 8 caracteres.")])
    
    def validate_fecha(form, field):
        if form.fecha_inicio.data and field.data:  # Verifica que ambas fechas existan
            if form.fecha_inicio.data > field.data:
                raise ValidationError("La fecha de inicio no puede ser mayor a la fecha de fin.")
            if field.data >= datetime.today().date():
                raise ValidationError("La fecha de fin no puede ser en el futuro.")
            if form.fecha_inicio.data <= (datetime.today().date().replace(year=datetime.today().year - 100)):
                raise ValidationError("La fecha de inicio no puede ser hace más de 100 años.")
            
    fecha_inicio = DateField("Fecha Inicio", validators=[DataRequired(message="La fecha de inicio es obligatoria."), validate_fecha])
    fecha_fin = DateField("Fecha Fin", validators=[DataRequired(message="La fecha de fin es obligatoria."), validate_fecha])
