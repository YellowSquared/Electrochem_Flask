from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class BathForm(FlaskForm):
    # A simple text input field with validation
    name = StringField('Name', validators=[DataRequired()])


    options = SelectField('Выберите вещество', choices=[],
                          validators=[DataRequired()])
    concentration = StringField('Выберите концентрацию грамм/литр (WIP)', validators=[DataRequired()])

    solvent = SelectField('Выберите растворитель', choices=[], validators=[DataRequired()])

    anode = SelectField('Выберите анод', choices=[], validators=[DataRequired()])

    cathode = SelectField('Выберите катод', choices=[], validators=[DataRequired()])

    # Submit button
    submit = SubmitField('Submit')

    electrodes = [

    ]
