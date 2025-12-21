from flask import Blueprint, render_template, flash, redirect, url_for

from electrochem_predict_flask import IonicCompound, IonicSolvent, Electrode, Bath, BathSoluteComponent, db, BathTemp
from electrochem_predict_flask.forms.bath_form import BathForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/predict', methods=['GET', 'POST'])
def predict():
    form = BathForm()
    form.solute.choices = [
        (compound.id, compound.get_formula() + ", " + compound.name)
        for compound in IonicCompound.query.all()
    ]
    form.solvent.choices = [
        (solvent.id, solvent.get_formula())
        for solvent in IonicSolvent.query.all()
    ]
    form.anode.choices = [
        (anode.id, anode.name)
        for anode in Electrode.query.all()
    ]
    form.cathode.choices = [
        (cathode.id, cathode.name)
        for cathode in Electrode.query.all()
    ]

    if form.validate_on_submit():
        compound_ids = form.solute.data
        solvent_id = form.solvent.data
        anode_id = form.anode.data
        cathode_id = form.cathode.data
        compound_ids.append(IonicCompound.query.filter_by(name="Ionised Water").first()) # TODO
        bath = BathTemp(Electrode.query.get(anode_id), Electrode.query.get(cathode_id), compound_ids)
        
        dominating_cation_reaction = bath.dominating_reduction_reaction()
        dominating_anion_reaction = bath.dominating_oxidation_reaction()

        return render_template('predict.html', form=form, 
                               dominating_cation_reaction=dominating_cation_reaction,
                               dominating_anion_reaction=dominating_anion_reaction)
    
    return render_template('predict.html', form=form)