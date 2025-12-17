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


class IonResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    potential_id = db.Column(db.Integer, db.ForeignKey('ion_potential.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=1.0)
    ion_id = db.Column(db.Integer, db.ForeignKey('ion.id'), nullable=True)

    ion = db.relationship("Ion", lazy=True)
    potential = db.relationship('IonPotential', back_populates='ion_results')


class CompoundResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    potential_id = db.Column(db.Integer, db.ForeignKey('ion_potential.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=1.0)
    compound_id = db.Column(db.Integer, db.ForeignKey(Compound.id), nullable=True)

    compound = db.relationship(Compound, lazy=True)
    potential = db.relationship('IonPotential', back_populates='compound_results')

class ElementResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    potential_id = db.Column(db.Integer, db.ForeignKey('ion_potential.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=1.0)
    element_id = db.Column(db.Integer, db.ForeignKey(Element.id), nullable=True)

    element = db.relationship(Element, lazy=True)
    potential = db.relationship('IonPotential', back_populates='element_results')


class IonPotential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ion_id = db.Column(db.Integer, db.ForeignKey('ion.id'), nullable=False)
    potential = db.Column(db.Float, nullable=False, default=0)

    ion = db.relationship('Ion', lazy=True)

    ion_results = db.relationship(IonResult, back_populates='potential')
    compound_results = db.relationship(CompoundResult, back_populates='potential')
    element_results = db.relationship(ElementResult, back_populates='potential')

    def get_results(self):
        return self.ion_results, self.compound_results, self.element_results


class Ion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    charge = db.Column(db.Integer)
    name = db.Column(db.String(50), unique=True, nullable=False)
    composition = db.relationship(IonElement, back_populates="ion", lazy=True)

    potentials = db.relationship(IonPotential, back_populates='ion')

    def is_anion(self) -> bool:
        return self.charge < 0

    def is_cation(self) -> bool:
        return self.charge > 0





