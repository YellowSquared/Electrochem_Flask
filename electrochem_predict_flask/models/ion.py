from flask_sqlalchemy import SQLAlchemy
from .compound import Compound
from .element import Element

from electrochem_predict_flask import db


class IonElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ion_id = db.Column(db.Integer, db.ForeignKey('ion.id'))
    element_id = db.Column(db.Integer, db.ForeignKey(Element.id), nullable=False)
    element_amount = db.Column(db.Float, nullable=False, default=1)
    element_charge = db.Column(db.Float)

    ion = db.relationship("Ion", lazy=True)
    element = db.relationship(Element, lazy=True)


class IonResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('ion_redox_result.id'))
    amount = db.Column(db.Float, nullable=False, default=1.0)
    ion_id = db.Column(db.Integer, db.ForeignKey('ion.id'), nullable=False)

    ion = db.relationship("Ion", lazy=True)
    result = db.relationship('IonRedoxResult', back_populates='ion_results')
    def get_formula(self):
        return self.ion.get_formula() #Todo


class CompoundResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('ion_redox_result.id'))
    amount = db.Column(db.Float, nullable=False, default=1.0)
    compound_id = db.Column(db.Integer, db.ForeignKey(Compound.id), nullable=False)

    compound = db.relationship(Compound, lazy=True)
    result = db.relationship('IonRedoxResult', back_populates='compound_results')
    def get_formula(self):
        return self.compound.get_formula() #Todo

class ElementResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('ion_redox_result.id'))
    amount = db.Column(db.Float, nullable=False, default=1.0)
    element_id = db.Column(db.Integer, db.ForeignKey(Element.id), nullable=False)

    element = db.relationship(Element, lazy=True)
    result = db.relationship('IonRedoxResult', back_populates='element_results')
    
    def get_formula(self):
        return self.element.sign #Todo


class IonRedoxResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    ion_results = db.relationship(IonResult, back_populates='result')
    compound_results = db.relationship(CompoundResult, back_populates='result')
    element_results = db.relationship(ElementResult, back_populates='result')

    def get_results(self):
        return self.ion_results, self.compound_results, self.element_results

    def get_formula(self):
        results_t = self.get_results()
        formulas = []
        for results in results_t:
            for result in results:
                formulas.append(result.get_formula())

        return ", ".join(formulas)


        


class IonRedoxReaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ion_id = db.Column(db.Integer, db.ForeignKey('ion.id'))
    potential = db.Column(db.Float, nullable=False, default=0)
    ion_amount = db.Column(db.Float, nullable=False, default=1)
    result_id = db.Column(db.Integer, db.ForeignKey(IonRedoxResult.id))

    # Defining the one-to-one relationship with result
    result = db.relationship(IonRedoxResult, backref='redox', foreign_keys=[result_id], uselist=False)
    ion = db.relationship('Ion', lazy=True)
    
    def __repr__(self):
        return f"{Ion.query.get(self.ion_id).get_formula()} -> {self.result.get_formula()}"



class Ion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    charge = db.Column(db.Integer)
    name = db.Column(db.String(50), unique=True, nullable=False)
    composition = db.relationship(IonElement, back_populates="ion", lazy=True)

    redox_potentials = db.relationship(IonRedoxReaction, back_populates='ion')

    def is_anion(self) -> bool:
        return self.charge < 0

    def is_cation(self) -> bool:
        return self.charge > 0

    def get_formula(self):
        formula = ""
        for comp in self.composition:
            formula += comp.element.sign

            if comp.element_amount == 1:
                continue
            elif comp.element_amount.is_integer():
                formula += str(int(comp.element_amount))
            else:
                formula += str(comp.element_amount)

        return formula