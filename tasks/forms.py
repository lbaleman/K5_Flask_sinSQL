from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, AnyOf
from wtforms.widgets import TextArea

from datetime import date


def greater_than_today(form, field):
    hoy = date.today()
    if field.data < hoy:
        raise ValidationError('La fecha debe ser superior o igual a hoy')

class TaskForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=3, max=15, message="La longitud ha de estar entre 3 y 15")])
    description = StringField('Descripcion', widget=TextArea())
    fx = DateField('Fecha', validators=[DataRequired(), greater_than_today])

    submit = SubmitField('Enviar')

class ProcessTaskForm(FlaskForm):
    ix = HiddenField('ix', validators = [DataRequired()])
    btn = HiddenField('btn', validators= [DataRequired(), AnyOf(['M','B'])])
    title = StringField('Título', validators=[DataRequired(), Length(min=3, max=15, message="La longitud ha de estar entre 3 y 15")])
    description = StringField('Descripcion', widget=TextArea())
    fx = DateField('Fecha', validators=[DataRequired(), greater_than_today])

    submit = SubmitField('Enviar')