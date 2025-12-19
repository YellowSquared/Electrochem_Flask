from flask import Blueprint, render_template, flash, redirect, url_for

from electrochem_predict_flask import IonicCompound, Solvent
from electrochem_predict_flask.forms.bath_form import BathForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/predict')
def predict():
    form = BathForm()

    form.options.choices = [
        (compound.id, compound.get_formula() + ", " + compound.name)
        for compound in IonicCompound.query.all()
    ]
    form.solvent.choices = [
        (solvent.id, solvent.compound.get_)
        for solvent in Solvent.query.all()
    ]

    if form.validate_on_submit():
        # Get the selected compound id (this would be the compound's id)
        selected_compound_id = form.options.data
        selected_compound = IonicCompound.query.get(selected_compound_id)
        flash(f'Selected compound: '
              f'{selected_compound.name} with formula: {selected_compound.get_formula()}', 'success')
        return redirect(url_for('main.index'))

    return render_template('predict.html', form=form)