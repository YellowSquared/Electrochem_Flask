from flask_sqlalchemy import SQLAlchemy
from .compound import Compound
from .element import Element

from app import db


class IonElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ion_id = db.Column(db.Integer, db.ForeignKey('ion.id'), nullable=False)
    element_id = db.Column(db.Integer, db.ForeignKey(Element.id), nullable=False)
    element_amount = db.Column(db.Float, nullable=False, default=1)

    ion = db.relationship("Ion", lazy=True)
    element = db.relationship(Element, lazy=True)



class IonPotential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ion_id = db.Column(db.Integer, db.ForeignKey('ion.id'), nullable=False)
    result_ion_id = db.Column(db.Integer, db.ForeignKey('ion.id'), nullable=True)
    result_compound_id = db.Column(db.Integer, db.ForeignKey(Compound.id), nullable=True)
    result_element_id = db.Column(db.Integer, db.ForeignKey(Element.id), nullable=True)
    potential = db.Column(db.Float, nullable=False)

    ion = db.relationship("Ion", lazy=True)
    result_ion = db.relationship("Ion", lazy=True)
    result_compound = db.relationship(Compound, lazy=True)
    result_element = db.relationship(Element, lazy=True)

class Ion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    charge = db.Column(db.Integer)
    name = db.Column(db.String(50), unique=True, nullable=False)
    composition = db.relationship(IonElement, lazy=True)
    potentials = db.relationship(IonPotential, foreign_keys=IonPotential.ion_id)





