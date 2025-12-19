from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class BathForm(FlaskForm):
    options = SelectField('Выберите вещество', choices=[],
                          validators=[DataRequired()])
    concentration = StringField('Укажите концентрацию (грамм/литр) (WIP)', validators=[DataRequired()])

    solvent = SelectField('Выберите растворитель', choices=[], validators=[DataRequired()])

    anode = SelectField('Выберите анод', choices=[], validators=[DataRequired()])

    cathode = SelectField('Выберите катод', choices=[], validators=[DataRequired()])

    # Submit button
    submit = SubmitField('Submit')
