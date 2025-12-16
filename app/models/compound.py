from app import db
from .element import Element

class CompoundElementComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compound_id = db.Column(db.Integer, db.ForeignKey("compound.id"))
    element_id = db.Column(db.Integer, db.ForeignKey(Element.id), nullable=False)
    element_amount = db.Column(db.Float, nullable=False)

    element = db.relationship(Element, lazy=True)
    compound = db.relationship("Compound", lazy=True)

class Compound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    components = db.relationship(CompoundElementComponent, back_populates="compound", lazy=True)

