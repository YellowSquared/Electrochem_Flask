from electrochem_predict_flask import db
from .element import Element


class CompoundElementComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compound_id = db.Column(db.Integer, db.ForeignKey("compound.id"))
    element_id = db.Column(db.Integer, db.ForeignKey(Element.id), nullable=False)
    element_amount = db.Column(db.Float, nullable=False, default=1)

    element = db.relationship(Element, lazy=True)
    compound = db.relationship("Compound", lazy=True)
    
    def get_formula(self):
        if isinstance(self.element_amount, float) and self.element_amount.is_integer():
            element_amount = int(self.element_amount)
        else:
            element_amount = self.element_amount

        if element_amount == 1:
            return self.element.sign
        return f"{self.element.sign}{element_amount}"

        


class Compound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    components = db.relationship(CompoundElementComponent, back_populates="compound", lazy=True)

    def get_formula(self):
        formulas = [component.get_formula() for component in self.components]
        return "".join(formulas)
        

