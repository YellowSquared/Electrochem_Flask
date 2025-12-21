from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, ValidationError
from electrochem_predict_flask.models import IonicCompound


def min_selections(min_count):
    def _min_selections(form, field):
        if len(field.data) < min_count:
            raise ValidationError()
    return _min_selections

class BathForm(FlaskForm):
    solute = QuerySelectMultipleField('Выберите вещество/вещества (Ctrl)', query_factory=lambda: IonicCompound.query.all(), validators=[DataRequired(), min_selections(1)])

    concentration = StringField('Укажите концентрацию вещества (грамм/литр) (WIP)', validators=[DataRequired()])

    solvent = SelectField('Выберите растворитель', choices=[], validators=[DataRequired()])

    anode = SelectField('Выберите анод', choices=[], validators=[DataRequired()])

    cathode = SelectField('Выберите катод', choices=[], validators=[DataRequired()])

    submit = SubmitField('Submit')
