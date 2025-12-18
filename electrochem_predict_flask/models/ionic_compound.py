from flask_sqlalchemy import SQLAlchemy
from .solvent import Solvent
from .ion import Ion
from electrochem_predict_flask import db


class Solubility(db.Model):
    ionic_compound_id = db.Column(db.Integer, db.ForeignKey("ionic_compound.id"), primary_key=True)
    solvent_id = db.Column(db.Integer, db.ForeignKey(Solvent.id), primary_key=True)
    value = db.Column(db.Float, nullable=False)

    solvent = db.relationship(Solvent, lazy=True)
    ionic_compound = db.relationship("IonicCompound", lazy=True)


class IonicComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ion_id = db.Column(db.Integer, db.ForeignKey(Ion.id), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=1)

    ion = db.relationship(Ion, lazy=True)


class IonicCompound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    cation_component_id = db.Column(db.Integer, db.ForeignKey(IonicComponent.id), nullable=False)
    anion_component_id = db.Column(db.Integer, db.ForeignKey(IonicComponent.id), nullable=False)

    solubility = db.relationship(Solubility, back_populates="ionic_compound", lazy=True)

    cation_component = db.relationship(IonicComponent, foreign_keys=[cation_component_id], lazy=True)
    anion_component = db.relationship(IonicComponent, foreign_keys=[anion_component_id], lazy=True)


    def get_formula(self):
        return self.cation_component.ion.get_formula() + self.anion_component.ion.get_formula()




